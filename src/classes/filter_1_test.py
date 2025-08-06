from filter_1 import Filter1
import spacy

# Test the filter
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_trf")
    test_text = """
For many decades, we’ve enriched foreign industry at the expense of American industry,
Subsidized the armies of other countries while allowing for the very sad depletion of our military.
We've defended other nation’s borders while refusing to defend our own,
And spent trillions of dollars overseas while America's infrastructure has fallen into disrepair and decay.

We’ve made other countries rich while the wealth, strength, and confidence of our country has disappeared over the horizon.
One by one, the factories shuttered and left our shores, with not even a thought about the millions upon millions of American workers left behind.
The wealth of our middle class has been ripped from their homes and then redistributed across the entire world.
But that is the past. And now we are looking only to the future.
We assembled here today are issuing a new decree to be heard in every city, in every foreign capital, and in every hall of power.
From this day forward, a new vision will govern our land.
From this moment on, it’s going to be America First.
Every decision on trade, on taxes, on immigration, on foreign affairs, will be made to benefit American workers and American families.
"""
    doc = nlp(test_text)
    
    # Create filter and run it
    filter1 = Filter1(doc)
    non_claim_doc, claim_doc = filter1.filter_claims()
    
    print("=== ORIGINAL TEXT ===")
    non_empty_sentences = [sent for sent in doc.sents if sent.text.strip()]
    print(f"Original sentences: {len(non_empty_sentences)}")
    for i, sent in enumerate(non_empty_sentences):
        print(f"{i+1}: {sent.text.strip()}")
    
    print("\n=== EXTRACTED CLAIMS ===")
    claim_sentences = list(claim_doc.sents)
    print(f"Found {len(claim_sentences)} claim sentences")
    if len(claim_sentences) > 0:
        for i, sent in enumerate(claim_sentences):
            print(f"{i+1}: {sent.text.strip()}")
    else:
        print("No claims found with current threshold")
    
    print("\n=== REMAINING NON-CLAIM SENTENCES ===")
    print(f"Remaining sentences: {len(list(non_claim_doc.sents))}")
    for i, sent in enumerate(non_claim_doc.sents):
        print(f"{i+1}: {sent.text.strip()}")
    
        # Directly checking sentence scores with full breakdown
    print(f"\n=== SENTENCE SCORES WITH BREAKDOWN ===")
    for i, sent in enumerate(non_empty_sentences):
        score = filter1._score_sentence(sent)
        is_claim = "CLAIM" if score >= filter1._score_threshold else "non-claim"
        print(f"{i+1}: {score:.1f} [{is_claim}] {sent.text.strip()}")
        
        # Full breakdown for each sentence
        print(f"   Named entities: {filter1._score_named_entities(sent):.1f}")
        print(f"   Quantifiable data: {filter1._score_quantifiable_data(sent):.1f}")
        print(f"   Strong structures: {filter1._score_strong_structures(sent):.1f}")
        print(f"   Temporal context: {filter1._score_temporal_context(sent):.1f}")
        print(f"   Factual indicators: {filter1._score_factual_indicators(sent):.1f}")
        print(f"   Economic policy: {filter1._score_economic_policy_language(sent):.1f}")
        print(f"   Question penalty: {filter1._score_is_question(sent):.1f}")
        print(f"   Hedging words: {filter1._score_hedging_words(sent):.1f}")
        print(f"   First person opinion: {filter1._score_first_person_opinion(sent):.1f}")
    