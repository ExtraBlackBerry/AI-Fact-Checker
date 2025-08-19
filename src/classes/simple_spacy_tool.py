# 28.07.25 John

import spacy as spc
from util import util

SIMILARITY_RATE = 0.5

class Spacy_Interface:
    def __init__(self, pipeline_type = "en_core_web_sm", disable_list = []): #"tagger", "attribute_ruler","parser"
        self._nlp = spc.load(pipeline_type, disable=disable_list)
        
    def get_nlp(self):
        return self._nlp

    def lemmatize_list(self, data_list, title):

        _result = []

        _title_doc = self._nlp(title)
        for doc in self._nlp.pipe(data_list, batch_size=32):
            _sim = _title_doc.similarity(doc)
            if _sim > SIMILARITY_RATE:
                _category_lemma_list = []
                for token in doc:
                    if not token.is_space and not token.is_punct:
                        _category_lemma_list.append(token.lemma_)
                    _category_lemma = " ".join(_category_lemma_list)
                _result.append(_category_lemma)

        return util.result(_result)
    
    def spacy_ner(self, title):
        _result = []
        _doc = self._nlp(title)
        for ent in _doc.ents:
            _result.append(ent.label_)
        _return = " ".join(_result)

        return util.result(_return)
        