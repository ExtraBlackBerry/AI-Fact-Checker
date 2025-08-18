# Foster 18/08/2025
# Class to extract a subject-predicate-object triplet from a spaCy Doc object.

class TripletExtractor:
    def __init__(self, doc):
        self._doc = doc
        self._sentences = [sent for sent in doc.sents if sent.text.strip()]

    def extract_triplets(self, text: str):
        """
        Extracts triplets from the given text.

        Args:
            text (str): The input text from which to extract triplets.
        """
        triplet = ""
        
        # Get sentence (each doc should have only one sentence anyway)
        if len(self._sentences) > 1:
            # TODO: REMOVE DEBUG PRINT
            print("Warning: More than one sentence in the document. Only the first sentence will be processed.")
        sentence = self._sentences[0]
        
        # --- Find Predicate ---
        # Find root verb (predicate)
        root_verb = None
        for token in sentence:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                root_verb = token
                break
            
        # If no root verb is found, return an empty list
        if not root_verb:
            # TODO: REMOVE DEBUG PRINT
            print("No root verb found in the sentence.")
            return []
        
        # --- Find Subject ---
        
        # --- Find object ---
        
        return triplet