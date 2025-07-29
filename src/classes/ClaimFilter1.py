# Foster 29/07/2025
# ClaimBuster API-based claim filtering component

from spacy.tokens import Doc, Span
from spacy.language import Language
import pandas as pd
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
CLAIM_PROBABILITIY_THRESHOLD = 0.5 # Scores over this threshold are considered claims
class ClaimFilter1:
    def __init__(self, doc: Doc):
        self._doc = doc
        self._sentences = [sent for sent in doc.sents]
        self._api_key = os.getenv('CLAIMBUSTER_API_KEY') # NEED api key in .env file
        self._score_threshold = CLAIM_PROBABILITIY_THRESHOLD
        self._filtered_claims_df = pd.DataFrame(columns=[
            "claim_text",           # The actual claim sentence/text
            "claimbusters_score",   # ClaimBuster's claim probability score
            "subject",              # Main entity/subject of the claim
            "pred",                 # Main verb or action in the claim
            "obj",                  # Object of the claim
            "sub_category",         # Wikipedia sub-category from token data
            "entities",             # Named entities in the claim
        ])

    def _filter_claims(self, doc: Doc):
        """
        Filters claims using ClaimBuster API.
        Returns:
            tuple: (remaining_doc, filtered_claims_df)
            remaining_doc (Doc): The original doc with claims removed
            filtered_claims_df (DataFrame): DataFrame with claims and their data for model training
        """
        claims_data = []
        sentences_to_keep = []
        
        for sentence in self._sentences:
            # Get ClaimBuster score for this sentence
            claim_score = self._get_claimbusters_score(sentence.text)
            
            if claim_score >= self._score_threshold:
                # This is a claim according to ClaimBuster
                claim_data = {
                    "claim_text": sentence.text.strip(),
                    "claimbusters_score": claim_score,
                    "subject": self._extract_subject(sentence),
                    "pred": None,         # TODO: Extract predicate verb
                    "obj": None,          # TODO: Extract object
                    "sub_category": None, # TODO: Extract sub-category from token data
                    "entities": [ent.text for ent in sentence.ents] # TODO: Get more info about entities
                }
                claims_data.append(claim_data)
            else:
                # Not a claim, keep in remaining doc
                sentences_to_keep.append(sentence)
        
        # Create DataFrame with claims
        self._filtered_claims_df = pd.DataFrame(claims_data)
        
        # Create filtered doc
        remaining_doc = self._create_filtered_doc(doc, sentences_to_keep)
        
        return remaining_doc, self._filtered_claims_df

    def _get_claimbusters_score(self, text: str) -> float:
        """
        Get claim probability score from ClaimBuster API.
        Returns:
            float: Probability score (0-1) that text contains a factual claim
        """
        try:
            # ClaimBuster API endpoint
            api_endpoint = "https://idir.uta.edu/claimbuster/api/v2/score/text/"
            
            # Request
            headers = {
                "x-api-key": self._api_key
            }
            payload = {
                "input_text": text
            }
            
            # Make API request
            response = requests.post(api_endpoint, json=payload, headers=headers)
            
            if response.status_code == 200: # 200 is success
                result = response.json()
                # Get score from json response
                return result.get("results", [{}])[0].get("score", 0.0)
            else:
                print(f"ClaimBuster API error: {response.status_code}")
                return 0.0
                
        except Exception as e:
            print(f"Error calling ClaimBuster API: {e}")
            return 0.0

    def _extract_subject(self, sentence: Span) -> str:
        """Extract the main subject of the claim"""
        # Find the subject (usually the first named entity or noun)
        for ent in sentence.ents:
            if ent.label_ in ['PERSON', 'ORG', 'GPE']:
                return ent.text
        
        # Use first noun as subject if no named entity found
        for token in sentence:
            if token.pos_ == 'NOUN' and not token.is_stop:
                return token.text
        
        return "Unknown"

    def _create_filtered_doc(self, original_doc: Doc, sentences_to_keep: list) -> Doc:
        """Create a new Doc with only non-claim sentences"""
        # If no sentences to keep, return empty doc
        if not sentences_to_keep:
            return Doc(original_doc.vocab) # needs vocab but is empty
        
        # For now, return original doc
        # TODO: Reconstruct doc with only non-claim sentences
        return original_doc

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
