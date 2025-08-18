# 06.08.25 John
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from classes.extractorAI import ExtractorAI

class Filter2:
    def __init__(self):
        self._vectorizer, self._main_model = joblib.load('Model/ExtractorAI.pkl')

    def _evaluate_text(self, docs):
        if not docs:
            return [],[]
        # _ent_num = []
        # _ent_text = []
        # _token_dep = []
        # _token_pos = []
        # _sentences = []
        # _combined = []
        # _doc = []

        claim_list = []
        non_claim_list = []

        for doc in docs:
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

            _vectorized = self._vectorizer.transform([(' '.join(_ent_t)) + ' ' + (' '.join(_token_d)) + ' ' +   (' '.join(_token_p)) + ' ' + str(_ent_n) + ' '.join(doc.text.split())])
            result = self._main_model.predict(_vectorized)
            if result == 1:
                claim_list.append(doc)
            else:
                non_claim_list.append(doc)

        return non_claim_list, claim_list