import spacy as spc

class Spacy_Interface:
    def __init__(self, pipeline_type = "en_core_web_sm", disable_list = []): #"tagger", "attribute_ruler","parser"
        self._nlp = spc.load(pipeline_type, disable=disable_list)
        
    def lemmatize_list(self, data_list):

        _result = []

        for doc in self._nlp.pipe(data_list, batch_size=32):
            _category_lemma_list = []
            for token in doc:
               if not token.is_space and not token.is_punct:
                   _category_lemma_list.append(token.lemma_)
            _category_lemma = " ".join(_category_lemma_list)
            _result.append(_category_lemma)

        return _result