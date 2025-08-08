# 05.08.25 John

import spacy as spc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from spacy.tokens import DocBin
from sklearn.manifold import TSNE
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer

class BaseModel:
    def __init__(self, jsonl_path):
        self._df = pd.read_json(jsonl_path, lines=True)
        

class ExtractorAI:
    def __init__(self, doc_bin_path,label_path):
        self._nlp = spc.load("en_core_web_trf") 

        self._vectorizer = TfidfVectorizer()

        self._labels = np.load(label_path)

        self._nlp = spc.load("en_core_web_trf")

        self._doc_bin = DocBin().from_disk(doc_bin_path)

        self._docs = list(self._doc_bin.get_docs(self._nlp.vocab))
        self._df = self._feature_extraction()
        self._model = self._set_cluster_model()
        self._fit_cluster_model()

    def _feature_extraction(self):

        _combined = []
        
        for doc in self._docs:
            _ent_n = 0
            _ent_t = []
            for ent in doc.ents:
                _ent_n += 1
                _ent_t.append(ent.label_.lower())

            _token_d = []
            _token_p = []
            for t in doc:
                _token_d.append(t.dep_.lower())
                _token_p.append(t.pos_.lower())
            
            _combined.append((' '.join(_ent_t)) + ' ' + (' '.join(_token_d)) + ' ' +   (' '.join(_token_p)) + ' ' + str(_ent_n) + ' '.join(doc.text.split()))
            
        return pd.DataFrame({
            'combined' : _combined
        })


    def _set_cluster_model(self):
        return SVC(kernel='linear', random_state=0)
    
    def _fit_cluster_model(self):
        _X_text = self._vectorizer.fit_transform(self._df['combined'])
        self._model.fit(_X_text, self._labels)
        joblib.dump((self._vectorizer, self._model), 'ExtractorAI.pkl')
    
    def visualize_clusters(self, n_components=2):
        _X_text = self._vectorizer.transform(self._df['combined'])
        _X_embedded = TSNE(n_components=n_components, random_state=0).fit_transform(_X_text.toarray())

        # Get predictions
        predicted_labels = self._model.predict(_X_text)

        plt.figure(figsize=(10, 8))
        plt.scatter(_X_embedded[:, 0], _X_embedded[:, 1], c=predicted_labels, cmap='viridis', s=50)
        plt.title('t-SNE visualization of predicted labels')
        plt.colorbar()
        plt.show()