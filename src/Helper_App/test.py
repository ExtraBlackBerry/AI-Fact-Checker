if __debug__:
    import sys
    import os

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


import torch
import spacy as spc
spc.prefer_gpu()

from src.classes.TextCatergorizer import custom_cat

from tqdm import tqdm

nlp = spc.load("en_core_web_trf") 
nlp.add_pipe("custom_categorizer", last=True)



text = """California has begun seeing its first tsunami waves with elevated water levels in Crescent City, in Northern California near the Oregon border.

A wave over 1 foot has been observed, according to data from the National Oceanic and Atmospheric Administration, with more waves expected soon.

The city is located along a 100-mile stretch of Northern California’s coast that is under a tsunami warning, the highest alert level. This area is under heightened tsunami risk because its unique underwater geography has the ability to “funnel wave energy,” according to the National Weather Service.

The rest of the US West Coast is under a tsunami advisory."""


df = pd.read_csv(r"D:\MyProj\PBT\PBT-FactCheckerApp\Datasets\all_sentences.csv") 
sentences = df["Text"].dropna().tolist()

doc = list(tqdm(nlp.pipe(sentences), total=len(sentences)))

embeddings = []

for d in doc:
    embeddings.append(d.vector.get())

np_emb = np.array(embeddings)
np.save("spacy_embeddings.npy", np_emb)

# for d in doc:
#     ner_emb = []
#     sub = []


#     for ent in d.ents:
#         ner_emb.append(ent.label_)
#         sub.append(ent.sub_category)


#     subcategory_encoder = OneHotEncoder(sparse=False, handle_unknown="ignore")
#     subcategory_encoder.fit(sub)

#     ner_encoder = OneHotEncoder(sparse=False, handle_unknown="ignore")
#     ner_encoder.fit(ner_emb)

#     ner_vec = np.zeros(len(ner_encoder.categories_[0]))
#     sub_vec = np.zeros(len(subcategory_encoder.categories_[0]))

#     embeddings.append(np.concatenate([sub_vec, ner_vec, d.vector]))

