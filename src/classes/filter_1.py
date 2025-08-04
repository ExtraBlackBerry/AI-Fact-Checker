# Foster 04/08/2025
# Rule based claim filtering component
from spacy.tokens import Doc, Span
from spacy.language import Language
import pandas as pd
import re

# RESEARCH TODO: Look into, using sliding window(look at nearby words), scoring POS patterns
# Statistical patterns detection, economic/policy language for political stuff

class Filter1:
    def __init__(self, doc: Doc, score_threshold: float = 3.0):
        """
        Initializes the filter with a document and a score threshold.
        Args:
            doc (Doc): The spaCy document to filter.
            score_threshold (float): Threshold for claim probability scores.
        """
        self._score_threshold = score_threshold
        self._doc = doc
        # Filter out empty/whitespace-only sentences
        self._sentences = [sent for sent in doc.sents if sent.text.strip()]
        self._filtered_claims_df = pd.DataFrame(columns=[
            "text",  # The text of the claim
            "score",  # The score of the claim
            # TODO: What do we want to give to the model?
        ])
        

    def filter_claims(self):
        """
        The main method to filter claims from the document.  
        It scores each sentence and separates claims from non-claims.  
        Called by the custom component in spaCy pipeline.  
        Returns:
            Tuple[Doc, pd.DataFrame]: The remaining document and a DataFrame of filtered claims.
        """
        claims_data = []
        sentence_docs_to_keep = []
        
        for sentence in self._sentences:
            score = self._score_sentence(sentence)
            if score >= self._score_threshold:
                claim_data = {
                    "text": sentence.text,
                    "score": score,
                    # TODO: Remember to update here as well when more added to claims DataFrame
                }
                # Is claim, add to df for model training
                claims_data.append(claim_data)
            else:
                # Not claim, create individual doc for sentence to recreate full doc and keep attributes
                sentence_doc = sentence.as_doc()
                sentence_docs_to_keep.append(sentence_doc)
                
        # Create df from claims data
        self._filtered_claims_df = pd.DataFrame(claims_data)
        
        # Create a new doc with the sentences that are not claims
        if sentence_docs_to_keep:
            remaining_doc = Doc.from_docs(sentence_docs_to_keep, ensure_whitespace=True)
        else:
            # If no sentences to keep, create empty doc with same vocab
            remaining_doc = Doc(self._doc.vocab)
        
        return remaining_doc, self._filtered_claims_df
        
    def _score_sentence(self, sentence: Span) -> float:
        """
        Scores a sentence based on predefined rules.
        Args:
            sentence (Span): The sentence to score.
        Returns:
            float: The score for the sentence.
        """
        score = 0.0
        
        # Score based on various criteria
        score += self._score_named_entities(sentence)
        score += self._score_quantifiable_data(sentence)
        score += self._score_strong_structures(sentence)
        score += self._score_temporal_context(sentence)
        score += self._score_factual_indicators(sentence)
        score += self._score_economic_policy_language(sentence)
        score += self._score_is_question(sentence)
        score += self._score_hedging_words(sentence)
        score += self._score_first_person_opinion(sentence)
        
        return score

    def _score_named_entities(self, sentence: Span) -> float:
        """
        Scores the named entities in a sentence.
        Args:
            sentence (Span): The sentence to score.
        Returns:
            float: The score based on named entities.
        """
        named_entities = [ent.label_ for ent in sentence.ents]
        score = 0.0
        
        # Sentences about people, organizations, locations, etc. are more likely to be claims i think
        # They are split up so the scores can be adjusted individually
        # Could maybe increment for each instance of an entity so like multiple people in a sentence
        if "PERSON" in named_entities:
            score += 1.5
        if "ORG" in named_entities:
            score += 1.5
        if "GPE" in named_entities:
            score += 1.5
            
        if "PRODUCT" in named_entities:
            score += 1.0
        if "EVENT" in named_entities:
            score += 1.0
        if "WORK_OF_ART" in named_entities:
            score += 1.5
            
        return score
    
    def _score_quantifiable_data(self, sentence: Span) -> float:
        """
        Increments score if the sentence contains quantifiable data.
        Args:
            sentence (Span): The sentence to score.
        Returns:
            float: The score based on quantifiable data
        """
        score = 0.0
        sentence_text = sentence.text.lower()
        
        # Standard spaCy named entities for quantities
        for ent in sentence.ents:
            if ent.label_ in ["DATE", "TIME", "PERCENT", "MONEY", "QUANTITY", "CARDINAL"]:
                score += 1.5

        # check for economic quantities that spaCy might miss
        # TODO: Add regex patterns for "trillions of dollars", "millions of workers"

        return score

    def _score_strong_structures(self, sentence: Span) -> float:
        """
        Scores any subject-verb-object or passive subject-verb-agent structures in a sentence.
        Args:
            sentence (Span): The sentence to score.
        Returns:
            float: The score based on structures found.
        """
        # TODO: Think about how to check for these with POS tags or maybe _dep
        return 0.0 #SUBJECT- VERB-OBJECT += 3 PASSIVE SUBJECT-VERB-AGENT += 3
    
    def _score_temporal_context(self, sentence: Span) -> float:
        """
        Scores the presence of temporal context in a sentence.
        Args:
            sentence (Span): The sentence to score.
        Returns:
            float: Score based on temporal references found.
        """
        sentence_text = sentence.text.lower()
        score = 0.0
        
        # Specific year patterns
        year_patterns = [
            r'\bin\s+\d{4}',     # "in 2023"
            r'\bsince\s+\d{4}',  # "since 2020"
            r'\bduring\s+\d{4}', # "during 2022"
            r'\bfrom\s+\d{4}',   # "from 2021"
            r'\buntil\s+\d{4}',  # "until 2024"
            r'\bby\s+\d{4}',     # "by 2025"
        ]
        
        for pattern in year_patterns:
            if re.search(pattern, sentence_text):
                score += 1.5
                break
        
        # Relative temporal phrases 
        relative_temporal = [
            "last year", "this year", "next year",
            "last month", "this month", "next month", 
            "last week", "this week", "next week",
            "last decade", "this decade", "next decade",
            "recent years", "coming years", "past years",
            "recently", "lately", "currently", "previously",
            "earlier this year", "later this year", "for many decades",
            "for many years", "for a long time", "in the past"
        ]
        
        for phrase in relative_temporal:
            if phrase in sentence_text:
                score += 1.0
                break
        
        return score
    
    def _score_factual_indicators(self, sentence: Span) -> float:
        """
        Scores the presence of factual indicator phrases in a sentence.
        Args:
            sentence (Span): The sentence to score.
        Returns:
            float: Score based on factual indicators found.
        """
        sentence_text = sentence.text.lower()
        score = 0.0
        strong_indicators = [
            "according to", "research shows", "studies indicate", "data reveals",
            "statistics show", "evidence suggests", "reports state", "findings show",
            "survey found", "analysis reveals", "investigation found", "study found",
            "research indicates", "data shows", "evidence indicates", "report shows"
        ]
        
        for indicator in strong_indicators:
            if indicator in sentence_text:
                score += 2.0
                break
            
        medium_indicators = [
            "experts say", "scientists believe", "researchers claim",
            "officials stated", "government data", "official records",
            "published study", "peer-reviewed", "clinical trial",
            "meta-analysis", "systematic review"
        ]
        
        for indicator in medium_indicators:
            if indicator in sentence_text:
                score += 1.5
                break
            
        weak_indicators = [
            "it is reported", "sources say", "allegedly", "reportedly",
            "claims that", "suggests that", "indicates that"
        ]
        
        for indicator in weak_indicators:
            if indicator in sentence_text:
                score += 0.5
                break
        
        return score
    
    def _score_economic_policy_language(self, sentence: Span) -> float:
        """
        Simple scoring for economic and policy language.
        Args:
            sentence (Span): The sentence to score.
        Returns:
            float: Score based on economic/policy terms found.
        """
        sentence_text = sentence.text.lower()
        score = 0.0
        
        # Basic economic terms - just check if any are present
        # TODO: Expand this list with more industry-specific terms
        # maybe score multiple terms higher but not per
        basic_economic_terms = [
            "industry", "factories", "wealth", "trade", "infrastructure", 
            "military", "workers", "taxes", "spending"
        ]
        for term in basic_economic_terms:
            if term in sentence_text:
                score += 1.5
                break
        
        # Words that suggest economic policy changes
        # TODO: Add more action verbs
        # maybe different weights for different types of actions
        policy_actions = [
            "subsidized", "enriched", "spent", "redistributed", "shuttered",
            "reformed", "regulated", "invested"
            ]
        for action in policy_actions:
            if action in sentence_text:
                score += 1.0
                break
        
        return score
    
    def _score_is_question(self, sentence: Span) -> float:
        """
        Scores if the sentence is a question (just checking for '?').
        Wont work with speech-to-text data (unless it picks up punctuation but idk).
        Just adding because will be useful for text input.
        Args:
            sentence (Span): The sentence to score.
        Returns:
            float: -5 score if it's a question, otherwise 0.
        """
        return -5.0 if sentence.text.strip().endswith('?') else 0.0
    
    def _score_hedging_words(self, sentence: Span) -> float:
        """
        Scores the presence of hedging words in a sentence.
        Args:
            sentence (Span): The sentence to score.
        Returns:
            float: -2 if hedging words are present, otherwise 0.
        """
        # TODO: Add more hedging words https://knowadays.com/blog/hedging-language-when-to-use-it-and-when-to-avoid-it/
        hedging_words = ["might", "could", "may", "possibly", "perhaps", "believe",
                         "think", "feel", "seem", "suggest"]
        return -2.0 if any(word in sentence.text.lower() for word in hedging_words) else 0.0
    
    def _score_first_person_opinion(self, sentence: Span) -> float:
        """
        Scores the presence of first-person opinion in a sentence.
        Args:
            sentence (Span): The sentence to score.
        Returns:
            float: -2.5 if first-person opinion is present, otherwise 0.
        """
        sentence_text = sentence.text.lower()
        
        # Check for first-person opinion phrases
        opinion_phrases = ["i think", "i believe", "i feel", "i guess", "i suppose", 
                          "in my opinion", "my view is", "i would say", "i consider",
                          "we think", "we believe", "we feel", "our opinion"]
        
        for phrase in opinion_phrases:
            if phrase in sentence_text:
                return -2.5
        # TODO: Maybe check for first person pronouns like "I", "we", "my", "our"? for less penalty
        return 0.0
        
        
# Custom component
@Language.component("claim_filter1")
def claim_filter1_component(doc: Doc):
    filter1 = Filter1(doc)
    return filter1.filter_claims()

