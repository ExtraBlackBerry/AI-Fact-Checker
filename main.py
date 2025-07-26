import spacy as spc

nlp = spc.load("en_core_web_trf") 

text = """Kiwi singer Hayley Westenra says she is “completely heartbroken” after learning her two long-time friends were killed in their home in Los Angeles.

American Idol music supervisor Robin Kaye, 70, and her husband Tom De Luca, 70, were discovered dead in their Encino home by police on July 14, the Los Angeles Police Department (LAPD) said in a statement.

The incident occurred four days earlier, on July 10.

A day after the bodies were found, authorities arrested 22-year-old Encino resident Ramond Boodarian, the LAPD confirmed.

This week, Westenra, 38, took to social media to express her shock and sadness."""

doc = nlp(text)
sentences = [sent for sent in doc.sents]

root_verb = None
predicate = None
obj = None
subject = None
check = None

for i, sentence in enumerate(sentences):

    print(f"{i+1}: {sentence}")
    
    for token in sentence:
        if token.dep_ in ("nsubj", "nsubjpass"):
            subject = token.text
            predicate = token.head.text
        #     print(f"{token.text}")
        #     print(f"{token.head.text}")

            for child in token.head.children:    
                if child.dep_ in ("prep", "dobj", "acomp", "oprd"):
                    for grandchildren in child.children:
                        if grandchildren.dep_ == "pobj":
                            check = grandchildren.text
                    obj = child.text
                    break

       
            print(subject, predicate, obj, check)
            obj = None
            check = None
                    
            
        #print(child.text, ", ")


            
    # for token in sentence:
    #     print("text: ",token.text,"| Dep_: ", token.dep_,"| Head.text: ", token.head.text,"| Head.pos_: ", token.head.pos_,
    #             [child for child in token.children])


#for ent in doc.ents:
    #print(ent.text, ent.label_)
    
#print(root_verb)
