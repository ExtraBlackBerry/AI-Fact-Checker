#John
import torch
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from classes.duckduckgo_search import google_search
from classes.triplet_extractor import InfoExtractor
import spacy

tokenizer = RobertaTokenizer.from_pretrained('Dzeniks/roberta-fact-check')
model = RobertaForSequenceClassification.from_pretrained('Dzeniks/roberta-fact-check')
nlp = spacy.load("en_core_web_md")
tripExtractor = InfoExtractor()

def classify_claim(claim, snippet):
    x = tokenizer.encode_plus(claim, snippet, return_tensors="pt")

    model.eval()
    with torch.no_grad():
        prediction = model(**x)

    label = torch.argmax(prediction[0]).item()
    return label

def get_snippet(claim, url):

    # extracting triplets
    tripExtractor.set_doc(claim)
    print("\nFull dependency tree:")

    for token in claim:
        print(f"{token.text:12} -> {token.dep_:10} | head: {token.head.text:12} | children: {[child.text for child in token.children]}")
        
    triplet = tripExtractor.extract_info()
    print(triplet)
    
    doc_claim = nlp(triplet)
    links = []
    focus = []
    for token in doc_claim:
            if token.dep_ == "nsubj":
                focus.append(f'"{token.text}"')

    results = google_search(claim ,(" ".join(focus)))
    if not results:
        print("No results found.")
        return 0,[]
    score = 0
    for r in results:
        if r['link'] == url:
            continue
        doc = nlp(r["snippet"])
        doc2 = nlp(r["title"])
        
        _sim = doc_claim.similarity(doc)
        _sim2 = doc_claim.similarity(doc2)

        if _sim > 0.3 and _sim2 > 0.1:
            label = classify_claim(claim, r["snippet"])
            if label == 0:
                score += (1 * _sim + _sim2) / 2
                links.append(r["link"])
            if label == 1:
                score += 0.01
        # if _sim2 > 0.8 and r["link"] not in links:
        #     links.append(r["link"])
        # if _sim > 0.8 and r["link"] not in links:
        #     links.append(r["link"])

    return score, links