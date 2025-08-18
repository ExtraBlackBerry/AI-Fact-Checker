# Foster 18/08/2025
# Class to extract a subject-predicate-object triplet from a spaCy Doc object.

class TripletExtractor:
    def __init__(self, doc):
        self._doc = doc
        self._sentences = [sent for sent in doc.sents if sent.text.strip()]
        self._predicate = None

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
        predicate = self._extract_predicate()
        if predicate == "":
            print("DEBUG: No predicate found in the sentence.")
        
        # Extract the subject
        subject = self._extract_subject()
        if subject == "":
            print("DEBUG: No subject found for the predicate.")
        
        # Extract the object
        object = self._extract_object()
        if object == "":
            print("DEBUG: No object found for the predicate.")
            
        # Construct the triplet
        triplet = f"{subject} {predicate} {object}"
        return triplet
    
    def _extract_predicate(self):
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
                self._predicate = token
                break
            
        # If no root verb is found, return an empty string
        if not predicate:
            print("DEBUG: No root verb found in the sentence.")
            predicate = ""
        
        return predicate
    
    def _extract_subject(self):
        """
        Extracts the subject from the predicates dependents.
        
        Args:
            predicate (Token): The predicate token from which to extract the subject.
        Returns:
            str: The extracted subject.
        """
        if not self._predicate:
            print("DEBUG: No predicate found to extract the object.")
            return ""
        
        # Look for nominal or passive subjects
        for child in self._predicate.children:
            if child.dep_ in ("nsubj", "nsubjpass"):
                return child.text # Return the subject text
            
        # If no subject is found, return an empty string
        print("DEBUG: No subject found for the predicate.")
        return ""
    
    def _extract_object(self):
        # Make sure theres a predicate to extract the object from
        if not self._predicate:
            print("DEBUG: No predicate found to extract the object.")
            return ""
        
        # Look for direct or indirect objects
        for child in self._predicate.children:
            if child.dep_ in ["dobj", "iobj", "attr"]:
                    return child.text
            # Also check for prepositional phrases
            elif child.dep_ == "prep":
                for prep_child in child.children:
                    if prep_child.dep_ == "pobj":
                        return prep_child.text
                    
        return ""  # If no object is found, return an empty string
    