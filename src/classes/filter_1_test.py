from filter_1 import Filter1
import spacy

# Test the filter
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_trf")
    test_text = """
    I think the weather is nice today. According to recent studies, 75% of people prefer sunny weather.
    John went to Microsoft yesterday. The study found that sales increased by 20% in 2023.
    I believe ice cream is delicious. Climate change has caused temperatures to rise by 1.5 degrees since 1880.
    What time is the meeting? Research shows that remote work productivity increased during the pandemic.
    Apple Inc. released new products in September 2023. Maybe we should consider other options.
    """
    doc = nlp(test_text)
    
    # Create filter and run it
    filter1 = Filter1(doc, score_threshold=5.0)
    remaining_doc, claims_df = filter1.filter_claims()
    
    print("=== ORIGINAL TEXT ===")
    non_empty_sentences = [sent for sent in doc.sents if sent.text.strip()]
    print(f"Original sentences: {len(non_empty_sentences)}")
    for i, sent in enumerate(non_empty_sentences):
        print(f"{i+1}: {sent.text.strip()}")
    
    print("\n=== EXTRACTED CLAIMS ===")
    print(f"Found {len(claims_df)} claim sentences")
    if len(claims_df) > 0:
        # Print out df nice
        for _, row in claims_df.iterrows():
            print(f"Score {row['score']:.1f}: {row['text'].strip()}")
    else:
        print("No claims found with current threshold")
    
    print("\n=== REMAINING NON-CLAIM SENTENCES ===")
    print(f"Remaining sentences: {len(list(remaining_doc.sents))}")
    for i, sent in enumerate(remaining_doc.sents):
        print(f"{i+1}: {sent.text.strip()}")
    
    # Directly checking sentence scores
    print(f"\n=== SENTENCE SCORES ===")
    for i, sent in enumerate(non_empty_sentences):
        score = filter1._score_sentence(sent)
        is_claim = "CLAIM" if score >= filter1._score_threshold else "non-claim"
        print(f"{i+1}: {score:.1f} [{is_claim}] {sent.text.strip()}")