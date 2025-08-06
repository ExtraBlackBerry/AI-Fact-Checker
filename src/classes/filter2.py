# 06.08.25 John
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from extractorAI import ExtractorAI


class Filter2:
    def __init__(self):
        self._vectorizer, self._main_model = joblib.load('Model/ExtractorAI.pkl')

    def _evaluate_text(self, docs):
        _ent_num = []
        _ent_text = []
        _token_dep = []
        _token_pos = []
        _sentences = []
        _combined = []

        for doc in docs:
            _sentences.append(doc.text)
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
            
            _ent_num.append(_ent_n)
            _ent_text.append(' '.join(_ent_t))
            _token_dep.append(' '.join(_token_d))
            _token_pos.append(' '.join(_token_p))
            _combined.append((' '.join(_ent_t)) + ' ' + (' '.join(_token_d)) + ' ' +   (' '.join(_token_p)) + ' ' + str(_ent_n))
            
        self._df = pd.DataFrame({
            'entity_num' : _ent_num,
            'entity_label' : _ent_text,
            'token_dep' : _token_dep,
            'token_pos' : _token_pos,
            'sentences' : _sentences,
            'combined' : _combined
        })
        self._main_model

        _X_text = self._vectorizer.transform(self._df['combined'])
        result = self._main_model.predict(_X_text)
        for i,doc in enumerate(docs):
            print(doc.text, "and" ,result[i])
