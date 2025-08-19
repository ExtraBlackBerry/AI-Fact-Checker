#john
if __debug__:
    import sys
    import os

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import numpy as np
import pandas as pd

from spacy.tokens import DocBin
from src.classes.TextCatergorizer import custom_cat


import torch

print(torch.__version__)
print("CUDA available:", torch.cuda.is_available())

import spacy as spc
spc.prefer_gpu()

from tqdm import tqdm                                                               #just a library to visualize the progress

nlp = spc.load("en_core_web_trf") 
nlp.add_pipe("custom_categorizer", last=True)

df = pd.read_json("Datasets/ClaimBusterTrain.json") 
sentences = df["text"].dropna().tolist()
labels = df["label"].tolist()
np.save("Datasets/labels.npy", labels)


docs = list(tqdm(nlp.pipe(sentences), total=len(sentences)))

doc_bin = DocBin(store_user_data=True)

for doc in docs:
    doc_bin.add(doc)

doc_bin.to_disk("Datasets/text2doc.spacy")


