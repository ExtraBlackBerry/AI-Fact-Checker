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
        
        # Extract the predicate
        predicate = self._extract_predicate(sentence)
        if predicate == "":
            print("DEBUG: No predicate found in the sentence.")
        
        # Extract the subject
        
        # Extract the object
        
        return triplet
    
    def _extract_predicate(self, doc):
        """
        Extracts the predicate from the sentence.
        
        Args:
            doc (Doc): The spaCy Doc object containing the sentence.
        Returns:
            str: The extracted predicate.
        """
        sentence = self._sentences[0]
        predicate = ""
        
        # Find the root verb (predicate)
        for token in sentence:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                predicate = token.text
                break
            
        # If no root verb is found, return an empty string
        if not predicate:
            print("DEBUG: No root verb found in the sentence.")
            predicate = ""
        
        return predicate