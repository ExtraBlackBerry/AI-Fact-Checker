import spacy as spc
from numpy import dot
from numpy.linalg import norm
import itertools

token_pair = []

nlp = spc.load("en_core_web_trf") 

print(nlp.pipe_names)

doc = nlp("I went to the bank, The river bank.")

def cosine_similarity(v1, v2):
    return dot(v1, v2) / (norm(v1) * norm(v2))

tokens = [token for token in doc if not token.is_punct and not token.is_space]

vectors = doc._.trf_data.all_outputs[0].data

for token, vec in zip(doc, vectors):
    token_pair.append((token.text, vec))


sim = cosine_similarity(token_pair[4][1], token_pair[8][1])

print(token_pair[4][0], token_pair[8][0])

print(sim)

