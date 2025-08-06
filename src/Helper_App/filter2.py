# 06.08.25 John

# if __debug__:
#     import sys
#     import os

#     sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from ...src.classes.extractorAI import ExtractorAI


class Filter2:
    def __init__(self):
        self._main_model = joblib.load(r'Model\ExtractorAI.pkl')

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
            'combined' : _combined,
            'sub_cat' : []                                      #not yet added
        })
        self._main_model




if __name__ == "__main__":
    at_test = ExtractorAI(r"Datasets/text2doc.spacy")
    at_test.test_cluster()