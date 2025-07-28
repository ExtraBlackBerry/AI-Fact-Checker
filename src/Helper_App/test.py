if __debug__:
    import sys
    import os

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import spacy as spc
from src.classes.TextCatergorizer import custom_cat

nlp = spc.load("en_core_web_trf") 
nlp.add_pipe("custom_categorizer", last=True)

text = """I have three dollars in my pocket"""

doc = nlp(text)
sentences = [sent for sent in doc.sents]

root_verb = None
predicate = None
obj = None
subject = []
test = []

# for i, sentence in enumerate(sentences):

#     print(f"{i+1}: {sentence}")

#     for token in sentence:
#         print(f"{token.text} : {token.lemma_}")
        
#         if token.dep_ in ("nsubj", "nsubjpass"):

#             test.append(token.text)
#             subject = test

#             predicate = token.head.text
#         #     print(f"{token.text}")
#         #     print(f"{token.head.text}")

#             for child in token.head.children:    
#                 if child.dep_ in ["prep", "dobj", "acomp", "oprd"]:
#                     for grandchildren in child.children:
#                         if grandchildren.dep_ == "pobj":
#                             obj = grandchildren.text

#                     if child.dep_ != "prep":
#                         obj = child.text
#                     break

#             test = []

#             if subject:       
#                 print(subject, predicate, obj)


#             obj = None
#             check = None
        #print(child.text, ", ")

    # for token in sentence:
        
    #     print("text: ",token.text,"| Dep_: ", token.dep_,"| Head.text: ", token.head.text,"| pos_: ", token.pos_,
    #             [child for child in token.children])


for ent in doc.ents:
    print(ent.text, ent.label_, ent._.sub_category)
    
#print(root_verb)
