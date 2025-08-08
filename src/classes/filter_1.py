# Foster 04/08/2025
# Rule based claim filtering component
from spacy.tokens import Doc, Span
from spacy.language import Language
import pandas as pd
import re

# RESEARCH TODO: Look into, using sliding window(look at nearby words), scoring POS patterns
# Statistical patterns detection, economic/policy language for political stuff
# Break down scoring of sentences to debug
# How to extract claims from a sentence that has multiple claims?
# break down sentences with multiple claims into individual sentences and append the previous part of the sentence? idk

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
        self._sentences = [sent for sent in doc.sents if sent.text.strip()]
        

    def filter_claims(self):
        """
        The main method to filter claims from the document.  
        It scores each sentence and separates claims from non-claims.  
        Called by the custom component in spaCy pipeline.  
        Returns:
            Tuple[List[Doc], List[Doc]]: Lists of individual sentence docs for non-claims and claims.
        """
        non_claim_sentences = []
        claim_sentences = []
        
        for sentence in self._sentences:
            score = self._score_sentence(sentence)
            if score >= self._score_threshold:
                # Is claim
                sentence_doc = sentence.as_doc()
                claim_sentences.append(sentence_doc)
            else:
                # Not claim
                sentence_doc = sentence.as_doc()
                non_claim_sentences.append(sentence_doc)
        
        return non_claim_sentences, claim_sentences
        
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
        score += self.score_contradiction_markers(sentence)
        score += self._score_factual_relationships(sentence)
        score += self._score_definitive_statements(sentence)
        
        
        return score

    def _score_named_entities(self, sentence: Span) -> float:
        """
        Scores the named entities in a sentence.
        Args:
            sentence (Span): The sentence to score.
        Returns:
            float: The score based on named entities.
        """
        entity_counts = {}
        score = 0.0
        
        for ent in sentence.ents:
            entity_counts[ent.label_] = entity_counts.get(ent.label_, 0) + 1
            
        # High val ents
        high_value_entities = {
            "PERSON": 1.5, "ORG": 1.5, "GPE": 1.5,
            "WORK_OF_ART": 1.5, "LAW": 2.0, "EVENT": 1.0
        }
        
        # Medium value ents
        medium_value_entities = {
            "PRODUCT": 1.0, "LANGUAGE": 0.8, "NORP": 1.2
        }
        
        # Score the ents
        for entity_type, count in entity_counts.items():
            if entity_type in high_value_entities:
                # Score with diminishing returns for multiple of same type
                score += high_value_entities[entity_type] * min(count, 3) * 0.8**(count - 1) 
            elif entity_type in medium_value_entities:
                score += medium_value_entities[entity_type] * min(count, 2) * 0.8**(count - 1)
            
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
        
        for ent in sentence.ents:
            if ent.label_ in ["PERCENT", "MONEY", "QUANTITY", "CARDINAL"]:
                score += 1.5
            # Make sure words like "today", "moment" don't count as quantifiable
            elif ent.label_ in ["DATE", "TIME"]:
                # Only score if it's one of these
                if any(word in ent.text.lower() for word in ["year", "decade", "trillion", "billion", "million"]):
                    score += 1.5
                    
        # Frequency words spacy found not catching
        quantity_words = [
            "twice", "thrice", "once", "multiple times", "several times",
            "first", "second", "third", "last", "final", "initial",
            "more than", "less than", "over", "under", "approximately",
            "about", "around", "nearly", "almost"
        ]
        
        for word in quantity_words:
            if word in sentence.text:
                score += 1.0

        # Regex patterns spacy might not catch
        quantity_patterns = [
            r'\d+\s*(trillion|billion|million|thousand)',
            r'\d+(\.\d+)?\s*percent',
            r'\$\d+(\.\d+)?\s*(trillion|billion|million|thousand)?',
            r'\d+\s*times\s*(more|less|higher|lower)',
            r'increase[ds]?\s*by\s*\d+',
            r'decrease[ds]?\s*by\s*\d+',
            r'\d+\s*fold\s*(increase|decrease)',
            r'grew\s*by\s*\d+',
            r'fell\s*by\s*\d+'
        ]
        for pattern in quantity_patterns:
            if re.search(pattern, sentence.text.lower()):
                score += 1.0

        return score

    def _score_strong_structures(self, sentence: Span) -> float:
        """
        Scores any subject-verb-object or passive subject-verb-agent structures in a sentence.
        Args:
            sentence (Span): The sentence to score.
        Returns:
            float: The score based on structures found.
        """
        score = 0.0
        
        sentence_text = sentence.text.lower()
    
        # No bonues for sentences that are policy statements
        policy_indicators = ["will", "going to", "new decree", "new vision", "from this day", "from this moment"]
        has_policy_language = any(indicator in sentence_text for indicator in policy_indicators)
        if has_policy_language:
            return 0.0
        
        has_subject = False
        has_verb = False
        has_object = False
        is_passive = False
        
        for token in sentence:
            # Check for subjects
            if token.dep_ in ["nsubj", "nsubjpass"]:
                has_subject = True
                if token.dep_ == "nsubjpass":
                    is_passive = True
            
            # Check for main verbs
            if token.pos_ == "VERB" and token.dep_ in ["ROOT", "aux", "auxpass"]:
                has_verb = True
                
            # Check for objects
            if token.dep_ in ["dobj", "pobj", "iobj"]:
                has_object = True
        
        # Score based on structure
        if has_subject and has_verb and has_object:
            score += 2.0  # Complete SVO structure
            if is_passive:
                score += 1.0  # Bonus for passive (apparently more factual)
        elif has_subject and has_verb:
            score += 1.0  # At least subject-verb
        return score
    
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
            "military", "workers", "taxes", "spending", "armies"
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
        sentence_text = sentence.text.lower()
        
        # Hedging words
        strong_hedging = ["might", "could", "may", "possibly", "perhaps", "supposedly", "allegedly"]
        moderate_hedging = ["believe", "think", "feel", "seem", "appear", "suggest", "indicate"]
        weak_hedging = ["likely", "probably", "generally", "usually", "tends to"]
        
        for word in strong_hedging:
            if word in sentence_text:
                return -2.5
        for word in moderate_hedging:
            if word in sentence_text:
                return -2.0
        for word in weak_hedging:
            if word in sentence_text:
                return -1.0
        
        return 0.0
    
    def score_contradiction_markers(self, sentence: Span) -> float:
        """
        Scores the presence of contradiction markers in a sentence.
        Args:
            sentence (Span): The sentence to score.
        Returns:
            Score based on contradiction markers found.
        """
        sentence_text = sentence.text.lower()
    
        contradiction_markers = [
            "however", "but", "although", "despite", "nevertheless",
            "on the other hand", "conversely", "in contrast", "whereas",
            "while", "yet", "still", "nonetheless", "even though"
        ]
        
        for marker in contradiction_markers:
            if marker in sentence_text:
                return 1.0  # Positive score - contradictions often reference facts
        
        return 0.0
    
    def _score_first_person_opinion(self, sentence: Span) -> float:
        """
        Scores the presence of first-person opinion in a sentence.
        Args:
            sentence (Span): The sentence to score.
        Returns:
            float: -2.5 if first-person opinion is present, otherwise 0.
        """
        sentence_text = sentence.text.lower()
        score = 0.0
        
        # Phrases that indicate opinion
        strong_opinion_phrases = [
            "i think", "i believe", "i feel", "in my opinion", 
            "my view is", "i would say", "i consider"
        ]
        weak_opinion_phrases = [
            "i guess", "i suppose", "we think", "we believe", 
            "we feel", "our opinion"
        ]
        
        # Score for present phrases
        for phrase in strong_opinion_phrases:
            if phrase in sentence_text:
                return -3.0
        for phrase in weak_opinion_phrases:
            if phrase in sentence_text:
                return -1.5
            
        # Check for first-person pronouns with opinion verbs
        first_person_pattern = r'\b(i|we)\s+(think|believe|feel|suppose|guess|consider)\b'
        if re.search(first_person_pattern, sentence_text):
            score -= 2.0
        return 0.0
    
    def _score_factual_relationships(self, sentence: Span) -> float:
        """
        Scores factual relationship patterns commone in encyclopedic text.
        Args:
            sentence (Span): The sentence to score.
        Returns:
            float: Score based on factual relationships found.
        """
        sentence_text = sentence.text.lower()
        score = 0.0
        
        # Common factual patterns
        factual_patterns = [
        r'\bis\s+(a|an|the)\s+\w+',  # "X is a Y"
        r'\bwas\s+(a|an|the)\s+\w+', # "X was a Y" 
        r'\bstarred\s+in\b',         # "X starred in Y"
        r'\bappeared\s+in\b',        # "X appeared in Y"
        r'\bcreated\s+by\b',         # "X created by Y"
        r'\bwritten\s+by\b',         # "X written by Y"
        r'\bdirected\s+by\b',        # "X directed by Y"
        r'\bwon\s+the\b',            # "X won the Y"
        r'\bowned\s+by\b',           # "X owned by Y"
        r'\baired\s+on\b'            # "X aired on Y"
        ]
        for pattern in factual_patterns:
            if re.search(pattern, sentence_text):
                score += 1.5
                break # Only score once per sentence
        
        return score
    
    def _score_definitive_statements(self, sentence: Span) -> float:
        """
        Scores definitive factual statements, Copula verbs are a good indicator.
        Args:
            sentence (Span): The sentence to score.
        Returns:
            float: Score based on definitive statements found.
        """
        score = 0.0
        
        # https://en.wikipedia.org/wiki/Copula_(linguistics)
        # 'Be' is the base for copula verbs in English
        # Look for copula verbs
        for token in sentence:
            if token.lemma_ == "be" and token.pos_ == "AUX":
                score += 1.0
                break
        
        return score
        
        
# Custom component
@Language.component("claim_filter1")
def claim_filter1_component(doc: Doc):
    filter1 = Filter1(doc)
    return filter1.filter_claims()

