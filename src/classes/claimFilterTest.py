from ClaimFilter1 import ClaimFilter1
import pandas as pd
import spacy

# === TESTING ===
if __name__ == "__main__":
    import spacy
    print("=== ClaimFilter1 Component Test ===")
    nlp = spacy.load("en_core_web_trf")
    
    # Add the claim filter to the pipeline
    nlp.add_pipe("claim_filter1", last=True)
    print(f"Pipeline components: {nlp.pipe_names}")
    
    test_text = """
    The weather is nice today. Donald Trump won the 2016 presidential election.
    I think pizza is delicious. The unemployment rate is 3.7 percent according to recent data.
    What time is it? Climate change has caused global temperatures to rise by 1.1 degrees Celsius.
    Scientists report that the Arctic ice is melting faster than predicted.
    """
    
    print(f"\n=== Processing Text ===")
    print(f"Input text:\n{test_text.strip()}\n")
    doc = nlp(test_text)
    sentences = [sent for sent in doc.sents if sent.text.strip()]
    print(f"Total sentences: {len(sentences)}")
    
    # Check if filtered_claims extension exists
    if hasattr(doc._, 'filtered_claims') and doc._.filtered_claims is not None:
        filtered_claims_df = doc._.filtered_claims
        print("Filtered claims df exists in doc")
        print(f"Claims detected: {len(filtered_claims_df)}")
        # Display claims found
        if len(filtered_claims_df) > 0:
            print(f"\n=== Detected Claims ===")
            for idx, row in filtered_claims_df.iterrows():
                print(f"\nClaim {idx + 1}:")
                print(f"  Text: {row['claim_text']}")
                print(f"  Score: {row['claimbusters_score']:.3f}")
                print(f"  Subject: {row['subject']}")
                print(f"  Entities: {row['entities']}")
            
            # Show df structure
            print(f"\n=== DataFrame Info ===")
            print(f"Shape: {filtered_claims_df.shape}")
            print(f"Columns: {list(filtered_claims_df.columns)}")
        else:
            print("No claims detected with current threshold")
            
    else:
        print("No dffound in processed doc")
    print(f"\n=== Test Complete ===")