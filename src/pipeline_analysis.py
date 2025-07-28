import spacy

sample_text = """A fulltime pitch invasion was quickly aborted during the Mid Canterbury club rugby final on Saturday after the referee ruled the game wasn’t actually over.
According to Southern’s supporters were guilty of celebrating too early, thinking their team had won the senior final 23-21 after a replacement Ashburton Celtic back was tackled over the sideline with 80 minutes up on the clock.
Dozens of young children sprinted on the field in celebration, only to be sent back by the players when the referee said there was still one minute left."""

# Debug Display Options
display_all_info = True
display_transformer_info = False
display_tagger_info = False
display_parser_info = False
display_attribute_ruler_info = False
display_lemmatizer_info = False
display_ner_info = False
display_full_info = False

nlp = spacy.load("en_core_web_trf")

# === COMPONENT ANALYSIS ===

print(f"Pipeline Components: {nlp.pipe_names}")
doc = nlp(sample_text)

# - Component 1: Transformer -
vectors = doc._.trf_data.all_outputs[0].data
if display_transformer_info or display_all_info:
    print("\n=== Transformer Information ===\n")
    print("\nFirst 3 token vectors:")
    for i in range(3):
        print(f"Token {i} ({doc[i].text}): {vectors[i][:10]}...")

# - Component 2: Tagger -
if display_tagger_info or display_all_info:
    print("\n=== Tagger Information ===\n")
    for token in doc[:10]:
        print(f"{token.text}: {token.tag_} ({token.pos_})")
        
# - Component 3: Parser -
if display_parser_info or display_all_info:
    print("\n=== Parser Information ===\n")
    for token in doc[:10]:
        print(f"{token.text}: {token.dep_} -> {token.head.text}")

# - Component 4: AttributeRuler -
if display_attribute_ruler_info or display_all_info:
    print("\n=== AttributeRuler Information ===\n")
    for token in doc[:10]:
        print(f"{token.text}: morph={token.morph}, lemma={token.lemma_}")

# - Component 5: Lemmatizer -
if display_lemmatizer_info or display_all_info:
    print("\n=== Lemmatization Information ===\n")
    for token in doc[:10]:
        print(f"{token.text} -> {token.lemma_}")

# - Component 6: NER -
if display_ner_info or display_all_info:
    print("\n=== Named Entity Recognition Information ===\n")
    for ent in doc.ents:
        print(f"{ent.text}: {ent.label_} ({ent.start}-{ent.end})")
        
# Full pipeline token information
if display_full_info or display_all_info:
    print("\n=== Full Pipeline Token Information ===")
    
    sentences = [sent for sent in doc.sents if sent.text.strip()]
    for i, sentence in enumerate(sentences):
        print(f"\n=== Sentence {i+1} ===")
        
        for token in sentence:
            # Skip whitespace tokens
            if token.is_space or not token.text.strip():
                continue
                
            entity_text = ""
            # Show info if entity detected
            if token.ent_iob_ != "O":
                entity_text = f"(Entity: {token.ent_type_}({token.ent_iob_}))"
            # Print full token info
            print(f"{token.text} {entity_text}, POS: {token.pos_}  ,  Tag: {token.tag_}  ,  Dep: {token.dep_}  ,  Head: {token.head.text}  ,  Lemma: {token.lemma_}  ,  Morph: {token.morph}")
            