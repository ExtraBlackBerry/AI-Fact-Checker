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

    def _check_facts(self, text, url):
        doc = self._nlp(text)

        self._filter1._set_doc(doc)
        non_claim_temp1, claim_temp1 = self._filter1.filter_claims()

        non_claim_temp2, claim_temp2 = self._filter2._evaluate_text(non_claim_temp1)

        self.non_claims.extend(non_claim_temp2)

        self.claims.extend(claim_temp1)

        self.claims.extend(claim_temp2)

        results = []
        claims = []
        all_links = []

        if not self.claims:
            print("NO CLAIMS FOUND")
            return {
                "score": "NOTHING TO CHECK HERE"
            }

        test = " ".join([claim.text for claim in self.claims])

        for claim in self.claims:
            claims.append(claim.text)
            score,links = get_snippet(claim.text,url)
            results.append(score)
            all_links.extend(links)

        sum = 0
        for n in results:
            if isinstance(n, str):
                continue
            sum += n
        avg = sum / len(results) if results else 0
        return {
            "score": avg,
            "links": all_links
        }


    


    