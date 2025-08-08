from filter_1 import Filter1
from filter2 import Filter2
import spacy
import pandas as pd

show_scores = True

# Test the filter
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_trf")

    df = pd.read_json("Datasets/train.jsonl", lines=True)

    texts = df["claim"]
    label = df["verifiable"]

    _true_true = 0
    _true_false = 0
    _false_true = 0
    _false_false = 0

    _true_true2 = 0
    _true_false2 = 0
    _false_true2 = 0
    _false_false2 = 0

    non_claim_list, claim_list = [], []
    non_claim_list2, claim_list2 = [],[]

    for i, text in enumerate(texts):
        doc = nlp(text)
        
        # Create filter and run it
        filter1 = Filter1(doc)
        non_claim_list, claim_list = filter1.filter_claims()
        
        if show_scores:
            print("========= Filter 1 score breakdown =========")
            for sent in doc.sents:
                print(f"Sentence: {sent.text}")
                print(f"Score for named entities: {filter1._score_named_entities(sent)}")
                print(f"Score for quantifiable data: {filter1._score_quantifiable_data(sent)}")
                print(f"Score for strong structures: {filter1._score_strong_structures(sent)}")
                print(f"Score for temporal context: {filter1._score_temporal_context(sent)}")
                print(f"Score for factual indicators: {filter1._score_factual_indicators(sent)}")
                print(f"Score for economic policy language: {filter1._score_economic_policy_language(sent)}")
                print(f"Score for is question: {filter1._score_is_question(sent)}")
                print(f"Score for hedging words: {filter1._score_hedging_words(sent)}")
                print(f"Score for first person opinion: {filter1._score_first_person_opinion(sent)}")
                print(f"Score for contradiction markers: {filter1.score_contradiction_markers(sent)}")
                print(f"Total score: {filter1._score_sentence(sent)}")
                print("===========================================")
            #score += self._score_named_entities(sentence)
            #score += self._score_quantifiable_data(sentence)
            #score += self._score_strong_structures(sentence)
            #score += self._score_temporal_context(sentence)f
            #score += self._score_factual_indicators(sentence)
            #score += self._score_economic_policy_language(sentence)
            #score += self._score_is_question(sentence)
            #score += self._score_hedging_words(sentence)
            #score += self._score_first_person_opinion(sentence)
            #score += self.score_contradiction_markers(sentence)
            print("===========================================")

        #filter2 testing
        filter2 = Filter2()
        non_claim_list2, claim_list2 = filter2._evaluate_text(non_claim_list)   
    
        if len(claim_list) > 0:
            for claim in claim_list:
                if label[i] == "VERIFIABLE":
                    _true_true += 1
                elif label[i] == "NOT VERIFIABLE":
                    _false_true += 1

        elif len(non_claim_list) > 0:
            # if len(non_claim_list) > 1:
            #     print("================================================================================")
            #     print(f"length of non_claim_list: {len(non_claim_list)}")
            #     print(non_claim_list)
            #     print("================================================================================")
            for claim in non_claim_list:
                if label[i] == "NOT VERIFIABLE":
                    _true_false += 1
                elif label[i] == "VERIFIABLE":
                    _false_false += 1


        if len(claim_list2) > 0:
            for claim in claim_list2:
                if label[i] == "VERIFIABLE":
                    _true_true2 += 1
                elif label[i] == "NOT VERIFIABLE":
                    _false_true2 += 1
        elif len(non_claim_list2) > 0:
            for claim in non_claim_list2:
                if label[i] == "NOT VERIFIABLE":
                    _true_false2 += 1
                elif label[i] == "VERIFIABLE":
                    _false_false2 += 1
    

        total = _false_false2 + _false_true2 + _true_true + _false_true + _true_true2 + _true_false2
        total_filter2 = _true_true2 + _true_false2 + _false_true2 + _false_false2

        # print(f"Total claims processed: {total}")
        # print(f"Correct Filter1: {_true_true}, Incorrect Filter1: {_false_true}")
        # print(f"Correct Filter1 NOT VARIFIABLE: {_true_false}, INCORRECT Filter1 NOT VARIFIABLE: {_false_false}")

        # print(f"Correct Filter2: {_true_true2}, Incorrect Filter2: {_false_true2}")
        # print(f"Correct Filter2 NOT VARIFIABLE: {_true_false2}, INCORRECT Filter2 NOT VARIFIABLE: {_false_false2}")

        print(f"Percentage Filter1: {(_true_true + _true_false) / (_false_false+_false_true+_true_false+_true_true) * 100:.2f}%")
        if total_filter2 > 0:
            print(f"Percentage Filter2: {(_true_true2 + _true_false2) / (_false_false2+_false_true2 +_true_false2+_true_true2) * 100:.2f}%")

        print(f"Total Correct extration: {(_true_true + _true_true2 + _true_false2) / total * 100:.2f}% claims")
        print(f"Total incorrect extraction: {(_false_true2 + _false_false2 + _false_true) / total * 100:.2f}% claims")
        


    