#John 18.08.25

from classes.filter_1 import Filter1
from classes.filter2 import Filter2
from classes.Checker2 import get_snippet  
import spacy
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

class FactCheckerAPI:
    def __init__(self):
        load_dotenv()
        self._nlp = spacy.load("en_core_web_trf")
        self._filter1 = Filter1()
        self._filter2 = Filter2()
        self.non_claims = []
        self.claims = []
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_response(self, prompt, text):
        response = self.client.responses.create(
            model="gpt-5-nano",
            input=f"""
            Please fact-check the following claim and give it a veracity score between 0 and 1, where 0 means completely false and 1 means completely true. 
            Provide a brief explanation for your score and evidence.:
            {prompt}

            This is the context text:
            {text}

            in your resonse, don't include any disclaimers or additional information, just provide the requested information in the specified.
            Don't refer to yourself. Don't mention AI model or any disclaimers.
            Don't use bullet points or lists.
            Don't repeat the claim in your response.
            Don't recommend any further actions.
            Don't include introductory or concluding remarks.

            response format:
            {{
                "score": float,
                "explanation": str,
                "evidence": str
            }}
            """,
        )

        return response.output[1].content[0].text

    def _check_facts(self, text, url):
        doc = self._nlp(text)

        self._filter1._set_doc(doc)
        non_claim_temp1, claim_temp1 = self._filter1.filter_claims()

        non_claim_temp2, claim_temp2 = self._filter2._evaluate_text(non_claim_temp1)

        self.non_claims.extend(non_claim_temp2)

        self.claims.extend(claim_temp1)

        self.claims.extend(claim_temp2)

        #results = []
        #claims = []
        all_links = []
        #ents_list = []
        if not self.claims:
            print("NO CLAIMS FOUND")
            return {
                "score": "NOTHING TO CHECK HERE"
            }

        print(f"Claims found: {[claim.text for claim in self.claims]}")

        returned_response = self.get_response("\n".join([claim.text for claim in self.claims]), text)
        data = json.loads(returned_response)

        print(f"Fact Check Response: {data}")

        # for claim in self.claims:
        #     for ents in claim.ents:
        #         if ents.label_ == "PERSON" or ents.label_ == "ORG" or ents.label_ == "GPE" or ents.label_ == "LOC" or ents.label_ == "PRODUCT":
        #             ents_list.append(f'"{ents.text}"')

        # test = " ".join([claim.text for claim in self.claims])

        # for claim in self.claims:
        #     claims.append(claim.text)
        #     score,links = get_snippet(claim.text ," ".join(ents_list), url)
        #     results.append(score)
        #     all_links.extend(links)

        # sum = 0
        # for n in results:
        #     if isinstance(n, str):
        #         continue
        #     sum += n
        # avg = sum / len(results) if results else 0
        return {
            "score": data.get("score", 0),
            "evidence": data.get("evidence", ""),
            "explanation": data.get("explanation", "")
        }


    


    