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
        
        # Iterate tokens and extract relevant parts based on dependency labels
        for token in self._doc:
            if token.dep_ in ["nsubj", "nsubjpass"]:
                # add children of the token if they are relevant
                for child in token.children:
                    if child.dep_ in ["amod", "compound"]:
                        parts.append(child.text)
                parts.append(token.text)
            elif token.dep_ in ["dobj", "pobj", "attr", "mark"]:
                parts.append(token.text)
            elif token.dep_ == "ROOT":
                parts.append(token.text)
            elif token.dep_ == "prep":
                parts.append(token.text)
            elif token.dep_ in ["amod", "advmod", "conj"]:
                parts.append(token.text)
            elif token.dep_ in ["aux", "neg"]:
                parts.append(token.text)
            elif token.dep_ == "relcl":
                parts.append(token.text)
                # Add children of the relative clause
                for child in token.children:
                    if child.dep_ in ["amod", "compound", "acomp"]:
                        parts.append(child.text)
            elif token.dep_ == "advcl":
                parts.append(token.text)
                
            # could maybe get children, lots in advcl
            # Maybe add nummod
            
        return " ".join(parts)
        
if __name__ == "__main__":
    import spacy
    nlp = spacy.load("en_core_web_trf")
    test_sentence = "Today it is up to about $38,000 of earnings that is subject to the payroll tax for Social Security"
    
    print(f"Input: {test_sentence}")
    
    doc = nlp(test_sentence)
    extractor = InfoExtractor()
    extractor.set_doc(doc)
    result = extractor.extract_info()
    print(f"Result: '{result}'")
    
    print("\nFull dependency tree:")
    for token in doc:
        print(f"{token.text:12} -> {token.dep_:10} | head: {token.head.text:12} | children: {[child.text for child in token.children]}")