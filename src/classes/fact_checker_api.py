#John 18.08.25

from classes.filter_1 import Filter1
from classes.filter2 import Filter2
from classes.Checker2 import get_snippet  
import spacy
import pandas as pd


class FactCheckerAPI:
    def __init__(self):
        self._nlp = spacy.load("en_core_web_trf")
        self._filter1 = Filter1()
        self._filter2 = Filter2()
        self.non_claims = []
        self.claims = []

    def _check_facts(self, text):
        doc = self._nlp(text)

        self._filter1._set_doc(doc)
        non_claim_temp1, claim_temp1 = self._filter1.filter_claims()

        non_claim_temp2, claim_temp2 = self._filter2._evaluate_text(non_claim_temp1)

        self.non_claims.extend(non_claim_temp2)
        self.claims.extend(claim_temp1)
        self.claims.extend(claim_temp2)

        claims = [str(c) for c in self.claims]
    
        results = []

        for claim in claims:
            score = get_snippet(claim)
            results.append(score)

        print(results)

        return {
            "claims": claims,
            "results": results  
        }


    


    