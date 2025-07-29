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
        self._filtered_claims_df = pd.DataFrame()

    def _filter_claims(self, doc: Doc):
        """
        Filters claims in the doc.
        Args:
            doc (Doc): The spaCy Doc object to filter.
        Returns:
            The filtered Doc with claims removed.  
            The filtered claims as a DataFrame for model training.
        """
        pass
    
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
    
# Custom component for spaCy pipeline
@Language.component("claim_filter1")
def claim_filter1_component(doc: Doc):
    _claim_filter1 = ClaimFilter1(doc)
    
    # Store filtered claims df in the doc for model training later
    if not Doc.has_extension("filtered_claims"):
        Doc.set_extension("filtered_claims", default=None)
    doc._.filtered_claims = _claim_filter1._filtered_claims_df
    
    return doc # Doc with claims filtered out to be passed to next component