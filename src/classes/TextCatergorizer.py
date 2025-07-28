
# 28.07.25 John
from spacy.tokens import Doc
from spacy.tokens import Span

from spacy.language import Language

from src.classes import sqlite
from src.util import util

NUMERIC_VALUE = ["CARDINAL", "DATE", "TIME", "MONEY", "ORDINAL", "PERCENT", "QUANTITY"]

class TextCatergorizer:
    def __init__(self, doc: Doc):
        self._sql = sqlite.SqliteDB()
        self._data_dict = {}
        self._sql.load_sqlite(self._data_dict)
        self._sentences = [sent for sent in doc.sents]
        self._doc = doc
        if not Span.has_extension("sub_category"):
            Span.set_extension("sub_category", default=None)


    def _value_checker(self):  
        for ent in self._doc.ents:
            if ent.label_ in NUMERIC_VALUE:
                pass
            else:
                if (ent.text.lower()) in self._data_dict.keys():
                    ent._.sub_category = self._data_dict[(ent.text.lower())]

        return self._doc
    

    def _numeric_classifier(self, ent):
        match ent.label_:
            case "CARDINAL":
                pass
            case "DATE":
                pass
            case "TIME":
                pass
            case "MONEY":
                pass
            case "ORDINAL":
                pass
            case "PERCENT":
                pass
            case "QUANTITY":
                pass




@Language.component("custom_categorizer")
def custom_cat(doc: Doc):
    _custom_cat = TextCatergorizer(doc)
    return _custom_cat._value_checker()