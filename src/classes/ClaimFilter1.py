# Foster 29/07/2025
# Rule based claim filtering component
# Takes doc as input and returns filtered claims as df for model training
# Passes rest of the doc not filtered as claims to next component

from spacy.tokens import Doc, Span
from spacy.language import Language
import pandas as pd

class ClaimFilter1:
    def __init__(self, doc: Doc):
        self._doc = doc
        self._sentences = [sent for sent in doc.sents]
        self._claims = []
        self._non_claims = []
        self._filtered_claims_df = pd.DataFrame(columns=[
            "claim_text",           # The actual claim sentence/text
            "subject",              # Main entity/subject of the claim
            "pred",                 # Main verb or action in the claim
            "obj",                  # Object of the claim
            "sub_category",         # Wikipedia sub-category from token data
            "entities",             # Named entities in the claim
        ])

    def _filter_claims(self, doc: Doc):
        """
        Filters claims in the doc.
        Args:
            doc (Doc): The spaCy Doc object to filter.
        Returns:
            tuple: (remaining_doc, filtered_claims_df)
                - remaining_doc: Doc with claim sentences removed
                - filtered_claims_df: DataFrame with filtered claims for training
        """
        claims_data = []
        sentences_to_keep = []
        
        for sentence in self._sentences:
            if self._contains_claim(sentence):
                # Extract claim data
                claim_data = {
                    "claim_text" : sentence.text.strip(),
                    "subject" : self._extract_subject(sentence),
                    "pred" : None,         # TODO: Extract predicate verb
                    "obj" : None,          # TODO: Extract object
                    "sub_category" : None, # TODO: Extract sub-category from token data
                    "entities" : [ent.text for ent in sentence.ents]
                }
                claims_data.append(claim_data) # Append claim data
            else:
                # Put non-claim sentences list to make filtered doc
                sentences_to_keep.append(sentence)
                
        # Add claims data to DataFrame
        self._filtered_claims_df = pd.DataFrame(claims_data)
        
        # Create a new Doc with only the sentences that are not claims
        remaining_doc = self._create_filtered_doc(doc, sentences_to_keep)
        
        return remaining_doc, self._filtered_claims_df
        
    def _contains_claim(self, sentence: Span) -> bool:
        """
        Determine if a sentence contains a claim.
        """
        return False
    
    def _filter_doc(self, doc: Doc) -> Doc:
        """
        Filter the Doc to remove sentences that are claims.
        Returns:
            Doc: The filtered Doc with claims removed.
        """
        return doc
    
    def _extract_subject(self, sentence: Span) -> str:
        """Extract the main subject of the claim"""
        # Find the subject (usually the first named entity or noun)
        for ent in sentence.ents:
            if ent.label_ in ['PERSON', 'ORG', 'GPE']:
                return ent.text
        
        # USe first noun as subject if no named entity found
        for token in sentence:
            if token.pos_ == 'NOUN' and not token.is_stop:
                return token.text
        
        return "Unknown"
    
    def _create_filtered_doc(self, original_doc: Doc, sentences_to_keep: list) -> Doc:
        """
        Create a new Doc with only the sentences that aren't claims.
        Args:
            original_doc (Doc): The original spaCy Doc.
            sentences_to_keep (list): List of sentences to keep in the new Doc.
        Returns:
            Doc: A new spaCy Doc with only the non-claim sentences.
        """
        if not sentences_to_keep:
            # Return empty doc if all sentences were claims
            return original_doc[:0]
        
        # TODO: Figure out how to reconstruct the Doc, just returning original for now
        return original_doc
    
# Custom component for spaCy pipeline
@Language.component("claim_filter1")
def claim_filter1_component(doc: Doc):
    _claim_filter1 = ClaimFilter1(doc)
    
    # Store filtered claims df in the doc for model training later
    if not Doc.has_extension("filtered_claims"):
        Doc.set_extension("filtered_claims", default=None)
    doc._.filtered_claims = _claim_filter1._filtered_claims_df
    
    return doc # Doc with claims filtered out to be passed to next component