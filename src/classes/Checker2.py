#John
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from classes.duckduckgo_search import search_articles
from classes.simple_spacy_tool import Spacy_Interface

tokenizer = RobertaTokenizer.from_pretrained('Dzeniks/roberta-fact-check')
model = RobertaForSequenceClassification.from_pretrained('Dzeniks/roberta-fact-check')
spacy_help = Spacy_Interface()
nlp = spacy_help.get_nlp()

def classify_claim(claim, snippet):
    x = tokenizer.encode_plus(claim, snippet, return_tensors="pt")

    model.eval()
    with torch.no_grad():
        prediction = model(**x)

    label = torch.argmax(prediction[0]).item()
    return label

def get_snippet(claim):
    results = search_articles(claim.text)
    if not results:
        return "No results found."
    score = 0
    for r in results:
        doc_claim = nlp(claim.text)
        doc = nlp(r["snippet"])
        
        _sim = doc.similarity(doc_claim)
        if _sim >= 0.35:
            print(_sim)
            label = classify_claim(claim.text, r["snippet"])
            print(f"Label for snippet '{r['snippet']}': {label}")
            if label == 0:
                score += 1
    return score
    