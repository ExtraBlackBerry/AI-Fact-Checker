# Foster 18/08/2025
# Class to extract a subject-predicate-object triplet from a spaCy Doc object.

class TripletExtractor:
    def __init__(self):
        self._doc = None
        self._sentences = None
        self._predicate = None
        
    def set_doc(self, doc):
        self._doc = doc
        self._sentences = [sent for sent in doc.sents if sent.text.strip()]

    def extract_triplets(self):
        triplet = ""
        
        # Extract the predicate
        predicate = self._extract_predicate()
        if predicate == "":
            print("DEBUG: No predicate found in the sentence.")
        
        # Extract the subject
        subject = self._extract_subject()
        if subject == "":
            print("DEBUG: No subject found for the predicate.")
        
        # Extract the object
        obj = self._extract_objects()
        if obj == "":
            print("DEBUG: No object found for the predicate.")
            
        # Construct the triplet
        triplet = f"{subject} {predicate} {obj}"
        return triplet
    
    def _extract_predicate(self):
        if not self._sentences:
            return ""
        
        sentence = self._sentences[0]
        predicate = ""
        
        # Find the root verb (predicate)
        for token in sentence:
            if token.dep_ == "ROOT" and token.pos_ in ["VERB", "AUX"]:
                predicate = self._extract_full_predicate_phrase(token)
                self._predicate = token
                break
        
        return predicate
    
    def _extract_subject(self):
        if not self._predicate:
            return ""
        
        # Look for nominal or passive subjects
        for child in self._predicate.children:
            if child.dep_ in ("nsubj", "nsubjpass"):
                return self._extract_full_noun_phrase(child)
        
        return "" # No subject found
    
    def _extract_objects(self):
        if not self._predicate or not self._sentences:
            return ""
        
        all_parts = []
        
        for token in self._sentences[0]:
            if token.dep_ == "prep":
                all_parts.append(token.text)
            elif token.dep_ in ["pobj", "dobj"]:
                all_parts.append(token.text)
            elif token.dep_ in ["amod", "nummod"]:
                all_parts.append(token.text)
            elif token.dep_ in ['advcl', 'advmod']: # Maybe remove these
                all_parts.append(token.text)
            elif token.dep_ in ["nsubj", "nsubjpass"]: # grabbing other subjects
                all_parts.append(token.text)
                for child in token.children:
                    if child.dep_ in ["det", "amod", "compound", "nummod"]:
                        all_parts.append(child.text)
        
        return " ".join(all_parts) if all_parts else ""
    
    def _extract_full_noun_phrase(self, token):
        
        # Get all children that modify the token
        modifiers = []
        for child in token.children:
            if child.dep_ in ["det", "amod", "compound", "nummod", "nmod", "prep", "poss"]:
                modifiers.append(child)
                # If its a preposition, get its children as well
                if child.dep_ == "prep":
                    for prep_child in child.children:
                        if prep_child.dep_ == "pobj":
                            modifiers.append(prep_child)
                # If its a numeric mod, get its children as well
                elif child.dep_ == "nummod":
                    for nummod_child in child.children:
                        if nummod_child.dep_ in ["compound", "det"]:
                            modifiers.append(nummod_child)
            
            # Get relative clauses, they hold additional information about the noun
            if child.dep_ == "relcl":
                for rel_child in child.children:
                    if rel_child.dep_ == "prep":
                        # Add the prep
                        modifiers.append(rel_child)
                        for prep_child in rel_child.children:
                            if prep_child.dep_ == "pobj":
                                # Add the object
                                modifiers.append(prep_child)
                                for pobj_child in prep_child.children:
                                    if pobj_child.dep_ in ["nummod", "amod", "compound"]:
                                        # Add any modifiers of the object
                                        modifiers.append(pobj_child)
                                        
                                        # Also get children of modifier to catch compound parts
                                        for mod_child in pobj_child.children:
                                            if mod_child.dep_ in ["compound", "punct"]:
                                                modifiers.append(mod_child)
                            
        # Sort modifiers by their position in the sentence
        modifiers.sort(key=lambda x: x.i)
        
        # Build the full noun phrase
        all_tokens = [token] + modifiers
        all_tokens.sort(key=lambda x: x.i)
        
        return " ".join([token.text for token in all_tokens])
    
    def _extract_full_predicate_phrase(self, token):
        # Split aux and mods into lists before and after the verb
        before_verb = []
        after_verb = []
        for child in token.children:
            if child.dep_ in ["aux", "auxpass", "neg"]:
                if child.i < token.i:
                    before_verb.append(child)
                else:
                    after_verb.append(child)

        # Sort each list by their position in the sentence
        before_verb.sort(key=lambda x: x.i)
        after_verb.sort(key=lambda x: x.i)
        
        # Build the full predicate phrase
        all_tokens = before_verb + [token] + after_verb
        
        return " ".join([token.text for token in all_tokens])
    
# Test the implementation
if __name__ == "__main__":
    import spacy
    nlp = spacy.load("en_core_web_trf")
    test_sentence = "One reason that crows and ravens are associated with death is because they would often follow armies as they marched to battle"
    
    print("Testing TripletExtractor:")
    print("=" * 60)
    print(f"Input: {test_sentence}")
    
    doc = nlp(test_sentence)
    extractor = TripletExtractor()
    extractor.set_doc(doc)
    result = extractor.extract_triplets()
    print(f"Result: '{result}'")
    
    print("\nFull dependency tree:")
    for token in doc:
        print(f"{token.text:12} -> {token.dep_:10} | head: {token.head.text:12} | children: {[child.text for child in token.children]}")