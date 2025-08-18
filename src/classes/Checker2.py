import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from classes.duckduckgo_search import search_articles

tokenizer = RobertaTokenizer.from_pretrained('Dzeniks/roberta-fact-check')
model = RobertaForSequenceClassification.from_pretrained('Dzeniks/roberta-fact-check')

def classify_claim(claim, snippet):
    x = tokenizer.encode_plus(claim, snippet, return_tensors="pt")

    model.eval()
    with torch.no_grad():
        prediction = model(**x)

    label = torch.argmax(prediction[0]).item()
    return label

def get_snippet(claim):
    results = search_articles(claim)
    if not results:
        return "No results found."
    score = 0
    for r in results:
        label = classify_claim(claim, r["snippet"])
        if label == 1:
            score += 1
    return score
    