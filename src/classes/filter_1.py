# Foster 04/08/2025
# Rule based claim filtering component
from spacy.tokens import Doc, Span
from spacy.language import Language
import pandas as pd

# RESEARCH TODO: Look into, using sliding window(look at nearby words), scoring POS patterns

class Filter1:
    def __init__(self, doc: Doc, score_threshold: float = 0.5):
        """
        Initializes the filter with a document and a score threshold.
        Args:
            doc (Doc): The spaCy document to filter.
            score_threshold (float): Threshold for claim probability scores.
        """
        self._score_threshold = score_threshold
        self._doc = doc
        self._sentences = [sent for sent in doc.sents]
        self._filtered_claims_df = pd.DataFrame(columns=[
            "text",  # The text of the claim
            "score",  # The score of the claim
            # TODO: What do we want to give to the model?
        ])
        
    from typing import Tuple

    def filter_claims(self) -> Tuple[Doc, pd.DataFrame]:
        """
        Filters claims from the document based on predefined rules.
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
        # Run all scoring functions and sum their scores
        pass

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
            score += 3.0
        if "ORG" in named_entities:
            score += 3.0
        if "GPE" in named_entities:
            score += 3.0
            
        if "PRODUCT" in named_entities:
            score += 2.0
        if "EVENT" in named_entities:
            score += 2.0
        if "WORK_OF_ART" in named_entities:
            score += 3.0
            
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
            if ent.label_ in ["DATE", "TIME", "PERCENT", "MONEY", "QUANTITY", "CARDINAL"]:
                score += 2.0

        return score

    def _score_strong_structures(self, sentence: Span) -> float:
        """
        Scores any subject-verb-object or passive subject-verb-agent structures in a sentence.
        Args:
            sentence (Span): The sentence to score.
        Returns:
            float: The score based on structures found.
        """
        pass #SUBJECT- VERB-OBJECT += 3 PASSIVE SUBJECT-VERB-AGENT += 3
    
    def _score_is_question(self, sentence: Span) -> float:
        """
        Scores if the sentence is a question (just checking for '?').
        Wont work with speech-to-text data (unless it picks up punctuation but idk).
        Just adding because will be useful for text input.
        Args:
            sentence (Span): The sentence to score.
        Returns:
            float: -10 score if it's a question, otherwise 0.
        """
        return -10.0 if sentence.text.strip().endswith('?') else 0.0
    
    def _score_hedging_words(self, sentence: Span) -> float:
        """
        Scores the presence of hedging words in a sentence.
        Args:
            sentence (Span): The sentence to score.
        Returns:
            float: -4 if hedging words are present, otherwise 0.
        """
        hedging_words = ["might", "could", "may", "possibly", "perhaps", "believe",
                         "think", "feel", "seem", "suggest"]
        return -4.0 if any(word in sentence.text.lower() for word in hedging_words) else 0.0
    
    def _score_first_person_opinion(self, sentence: Span) -> float:
        """
        Scores the presence of first-person opinion in a sentence.
        Args:
            sentence (Span): The sentence to score.
        Returns:
            float: -5 if first-person opinion is present, otherwise 0.
        """
        sentence_text = sentence.text.lower()
        
        # Check for first person view phrases
        # Maybe check for first person pronouns like "I", "we", "my", "our"? for less penalty
        pass
        
        # Custom component
@Language.component("claim_filter1")
def claim_filter1_component(doc: Doc):
    
    _claim_filter1 = ClaimFilter1(doc)
    # Run the filtering
    remaining_doc, filtered_claims_df = _claim_filter1._filter_claims(doc)
    
    # Store filtered claims df in the doc for model training later
    if not Doc.has_extension("filtered_claims"):
        Doc.set_extension("filtered_claims", default=None)
    doc._.filtered_claims = filtered_claims_df
    
    return remaining_doc  # Return doc with claims stored in extension