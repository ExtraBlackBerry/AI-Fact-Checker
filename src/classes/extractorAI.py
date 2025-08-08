# 05.08.25 John

import spacy as spc
import pandas as pd
import numpy as np
import joblib
from spacy.tokens import DocBin
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

class BaseModel:
    def __init__(self, jsonl_path):
        self._df = pd.read_json(jsonl_path, lines=True)
        

class ExtractorAI:
    def __init__(self, doc_bin_path, k = 2, random_seed = 0):
        self._nlp = spc.load("en_core_web_trf") 
        self._k = k
        self._random_seed = random_seed
        self._vectorizer = TfidfVectorizer()
        self._sub_cat_vec = {}
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
                _ent_t.append(ent.label_)
            _token_d = []
            _token_p = []
            for t in doc:
                _token_d.append(t.dep_)
                _token_p.append(t.pos_)
            
            _combined.append((' '.join(_ent_t)) + ' ' + (' '.join(_token_d)) + ' ' +   (' '.join(_token_p)) + ' ' + str(_ent_n))
            
        return pd.DataFrame({
            'combined' : _combined
        })


    def _set_cluster_model(self):
        return KMeans(n_clusters=self._k, random_state=self._random_seed)
    
    def _fit_cluster_model(self):
        _X_text = self._vectorizer.fit_transform(self._df['combined'])
        self._model.fit(_X_text)
        joblib.dump((self._vectorizer, self._model), 'ExtractorAI.pkl')
    
    def test_cluster(self, test_num):
        for i in range(test_num):
            if self._model.labels_[i] == 0:
                print("ID: ", i )
                print("Cluster ID: ", self._model.labels_[i])
                print("sentence: ", self._docs[i].text)
