from filter_1 import Filter1
from filter2 import Filter2
import spacy
import pandas as pd

# Test the filter
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_trf")

    df = pd.read_json("Datasets/ClaimBusterTest.json")

    texts = df["text"]
    label = df["label"]

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

        #filter2 testing
        filter2 = Filter2()
        non_claim_list2, claim_list2 = filter2._evaluate_text([doc])   
    
        if len(claim_list) > 0:
            for claim in claim_list:
                if label[i] == 1:
                    _true_true += 1
                elif label[i] == 0:
                    _false_true += 1

        elif len(non_claim_list) > 0:
            # if len(non_claim_list) > 1:
            #     print("================================================================================")
            #     print(f"length of non_claim_list: {len(non_claim_list)}")
            #     print(non_claim_list)
            #     print("================================================================================")
            for claim in non_claim_list:
                if label[i] == 0:
                    _true_false += 1
                elif label[i] == 1:
                    _false_false += 1


        if len(claim_list2) > 0:
            for claim in claim_list2:
                if label[i] == 1:
                    _true_true2 += 1
                elif label[i] == 0:
                    _false_true2 += 1
        elif len(non_claim_list2) > 0:
            for claim in non_claim_list2:
                if label[i] == 0:
                    _true_false2 += 1
                elif label[i] == 1:
                    _false_false2 += 1
    

        total = _false_false2 + _false_true2 + _true_true + _false_true + _true_true2 + _true_false2
        total_filter2 = _true_true2 + _true_false2 + _false_true2 + _false_false2

        # print(f"Total claims processed: {total}")
        # print(f"Correct Filter1: {_true_true}, Incorrect Filter1: {_false_true}")
        # print(f"Correct Filter1 NOT VARIFIABLE: {_true_false}, INCORRECT Filter1 NOT VARIFIABLE: {_false_false}")

        # print(f"Correct Filter2: {_true_true2}, Incorrect Filter2: {_false_true2}")
        # print(f"Correct Filter2 NOT VARIFIABLE: {_true_false2}, INCORRECT Filter2 NOT VARIFIABLE: {_false_false2}")
        if _false_false+_false_true+_true_false+_true_true > 0:
            print(f"Percentage Filter1: {(_true_true + _true_false) / (_false_false+_false_true+_true_false+_true_true) * 100:.2f}%")
        if total_filter2 > 0:
            print(f"Percentage Filter2: {(_true_true2 + _true_false2) / (_false_false2+_false_true2 +_true_false2+_true_true2) * 100:.2f}%")

        # print(f"Total Correct extration: {(_true_true + _true_true2 + _true_false2) / total * 100:.2f}% claims")
        # print(f"Total incorrect extraction: {(_false_true2 + _false_false2 + _false_true) / total * 100:.2f}% claims")




    