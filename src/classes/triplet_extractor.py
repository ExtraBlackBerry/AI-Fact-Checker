# Foster 18/08/2025
# Class to condense a sentence into its key information 

class InfoExtractor:
    def __init__(self):
        self._doc = None
        self._sentences = None
        
    def set_doc(self, doc):
        self._doc = doc
        self._sentences = [sent for sent in doc.sents if sent.text.strip()]

    def extract_info(self):
        if not self._doc or not self._sentences:
            return ""
        
        parts = []
        
        # Extract Named Entities
        entities = [ent.text for ent in self._doc.ents if ent.label_ in [
            "PERSON", "ORG", "GPE", "MONEY", "DATE", "EVENT", 
            "LAW", "PRODUCT", "WORK_OF_ART", "LANGUAGE"
        ]]
        parts.extend(entities)
        
        # Extract dep relationships
        entity_tokens = {token.i for ent in self._doc.ents for token in ent}
        
        for token in self._doc:
            # Skip if already captured as entity
            if token.i in entity_tokens:
                continue
                
            # Subject, object, and predicates
            if (token.dep_ in ["nsubj", "nsubjpass", "dobj", "ROOT"] and 
                token.pos_ in ["NOUN", "PROPN", "VERB"] and
                not token.is_stop):
                parts.append(token.lemma_)
            
            # Modifiers
            elif (token.dep_ in ["amod", "compound"] and 
                  token.pos_ in ["ADJ", "NOUN"] and
                  not token.is_stop):
                parts.append(token.lemma_)
        
        # Only keep single instances of terms
        unique_terms = []
        for term in parts:
            if term.lower() not in [t.lower() for t in unique_terms]:
                unique_terms.append(term)
        
        return " ".join(unique_terms)
        
if __name__ == "__main__":
    import spacy
    nlp = spacy.load("en_core_web_trf")
    test_sentence = "Cows have accents depending on where they’re born and they also have best friends and get depressed when separated."
    doc = nlp(test_sentence)
    extractor = InfoExtractor()
    extractor.set_doc(doc)
    search_result = extractor.extract_info()
    
    print(f"Input: {test_sentence}")
    print(f"Output: '{search_result}'")
    print("\nNamed Entities:")
    for ent in doc.ents:
        print(f"{ent.text:15} -> {ent.label_:10} ({spacy.explain(ent.label_)})") # type: ignore
    print("\nFull dependency tree:")
    for token in doc:
        print(f"{token.text:12} -> {token.dep_:10} | head: {token.head.text:12} | children: {[child.text for child in token.children]}")