import spacy as spc

nlp = spc.load("en_core_web_trf")

sentence = "Why Apple is looking at buying U.K. startup for $1 billion ?"
doc = nlp(sentence)

print([(w.text, w.pos_) for w in doc])