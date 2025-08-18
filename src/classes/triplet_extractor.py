# Foster 18/08/2025
# Class to extract a subject-predicate-object triplet from a spaCy Doc object.

class TripletExtractor:
    def __init__(self, doc): # TODO: Remove need for doc, copy johns (pretty sure just set doc method)
        self._doc = doc
        self._sentences = [sent for sent in doc.sents if sent.text.strip()]
        self._predicate = None

    def extract_triplets(self, text: str):
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
        obj = self._extract_object()
        if obj == "":
            print("DEBUG: No object found for the predicate.")
            
        # Construct the triplet
        triplet = f"{subject} {predicate} {obj}"
        return triplet
    
    def _extract_predicate(self):
        sentence = self._sentences[0]
        predicate = ""
        
        # Find the root verb (predicate)
        for token in sentence:
            if token.dep_ == "ROOT" and token.pos_ in ["VERB", "AUX"]:
                predicate = self._extract_full_predicate_phrase(token)
                self._predicate = token
                break
            
        # If no root verb is found, return an empty string
        if not predicate:
            predicate = ""
        
        return predicate
    
    def _extract_subject(self):
        if not self._predicate:
            return ""
        
        # Look for nominal or passive subjects
        for child in self._predicate.children:
            if child.dep_ in ("nsubj", "nsubjpass"):
                return self._extract_full_noun_phrase(child)
            
        # If no subject is found, return an empty string
        return ""
    
    def _extract_object(self):
        # Make sure theres a predicate to extract the object from
        if not self._predicate:
            return ""
        
        # Look for direct or indirect objects
        for child in self._predicate.children:
            if child.dep_ in ["dobj", "iobj", "attr"]:
                    return self._extract_full_noun_phrase(child)
            # Also check for prepositional phrases
            elif child.dep_ == "prep":
                for prep_child in child.children:
                    if prep_child.dep_ == "pobj":
                        return self._extract_full_noun_phrase(prep_child)
                    
        # For passive, look for oprd (object predicate)
        for child in self._predicate.children:
            if child.dep_ == "oprd":
                return self._extract_full_noun_phrase(child)
                    
        # For passive, also check for agents
        for child in self._predicate.children:
            if child.dep_ == "agent":
                for agent_child in child.children:
                    if agent_child.dep_ == "pobj":
                        return self._extract_full_noun_phrase(agent_child)
                    
        return ""  # If no object is found, return an empty string
    
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
            if child.dep_ in ["aux", "auxpass", "advmod", "neg"]:
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
    test_sentence = "The unemployment, the number of people who are still looking for work, is still 23 million Americans."
    
    print("Testing TripletExtractor:")
    print("=" * 60)
    print(f"Input: {test_sentence}")
    
    doc = nlp(test_sentence)
    extractor = TripletExtractor(doc)
    result = extractor.extract_triplets("")
    print(f"Result: '{result}'")
    
    print("\nFull dependency tree:")
    for token in doc:
        print(f"{token.text:12} -> {token.dep_:10} | head: {token.head.text:12} | children: {[child.text for child in token.children]}")