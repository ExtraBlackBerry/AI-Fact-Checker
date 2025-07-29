# 28.07.25 Foster
# Interface to manipulate the spacy pipeline and view results

if __debug__:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import spacy
from spacy.language import Language
from src.util import util
import src.config as configs


class PipelineInterface:
    """Interface for managing and analyzing a Spacy NLP pipeline."""
    
    def __init__(self, model_or_pipeline="en_core_web_trf"):
        # Dict to track custom/modified components
        self._custom_components = {}
        
        # If model_or_pipeline is a string, load the model
        if isinstance(model_or_pipeline, str):
            # It's a model name
            self._model_name = model_or_pipeline
            self._nlp = spacy.load(model_or_pipeline)
        else: # It's already a pipeline object
            self._nlp = model_or_pipeline
            self._model_name = getattr(model_or_pipeline, 'meta', {}).get('name', 'unknown')
        
    # === COMPONENT MANAGEMENT ===
    # https://spacy.io/usage/processing-pipelines#custom-components
    
    def add_new_custom_component(self, component_name, position="last", before=None, after=None):
        """Add a new custom component with its custom function to the pipeline. UNTESTED"""
        try:
            # Determine position arguments
            position_args = {}
            if position == "first":
                position_args["first"] = True
            elif position == "last":
                position_args["last"] = True
            elif before:
                position_args["before"] = before
            elif after:
                position_args["after"] = after
            
            # Add the custom component to the pipeline
            self._nlp.add_pipe(component_name, **position_args)
            return util.result(f"Successfully added custom component '{component_name}' to pipeline")
            
        except Exception as e:
            return util.error_code(500, f"Error adding custom component '{component_name}': {e}")
        
    def update_custom_component_function(self, component_name, new_function):
        """Update the function of an existing custom component. UNTESTED"""
        pass # TODO: implement
        
    def add_new_spacy_component(self, name, config_dict=None, position="last", before=None, after=None):
        """Add a new spacy pipe component to the pipeline from a string. 'lemmatizer', 'ner', 'tagger', etc. TESTING """
        try:
            # Determine position arguments
            position_args = {}
            if position == "first":
                position_args["first"] = True
            elif position == "last":
                position_args["last"] = True
            elif before:
                position_args["before"] = before
            elif after:
                position_args["after"] = after
            
            # Add the component
            self._nlp.add_pipe(name, config=config_dict, **position_args)
            return util.result(f"Successfully added component '{name}' to pipeline")

        except Exception as e:
            return util.error_code(501, f"Unexpected error adding spacy component '{name}': {e}")
    
    def remove_component(self, name):
        """Remove a component from the pipeline WORKING"""
        try:
            if name not in self._nlp.pipe_names:
                return util.error_code(502, f"Component '{name}' not found in pipeline")
            
            # Remove from pipeline
            self._nlp.remove_pipe(name)
            
            # Remove from custom components tracking if it exists
            if name in self._custom_components:
                del self._custom_components[name]
            
            return util.result(f"Successfully removed component '{name}' from pipeline")
            
        except Exception as e:
            return util.error_code(503, f"Error removing component '{name}': {e}")
        
    def modify_spacy_component(self, name, config_dict):
        """Modify an existing component in the pipeline. TESTING"""
        # Check if the component exists
        if name not in self._nlp.pipe_names:
            return util.error_code(504, f"Component '{name}' not found in pipeline")
        
        try:
            # Get the current component
            current_component = self._nlp.get_pipe(name)
            
            # Saving parts components need to be preserved
            # Lemmatizer needs lookup tables
            if name == "lemmatizer" and hasattr(current_component, 'lookups'):
                preserved_lookups = current_component.lookups
            
            # Get the current position of the component
            pipe_names = list(self._nlp.pipe_names)
            component_index = pipe_names.index(name)
            
            # Determine position arg for re-adding
            if component_index == 0:
                position_args = {"first": True}
            elif component_index == len(pipe_names) - 1:
                position_args = {"last": True}
            else:
                previous_component = pipe_names[component_index - 1]
                position_args = {"after": previous_component}
            
            # Remove the component
            self._nlp.remove_pipe(name)
            # Add the component back with new config
            self._nlp.add_pipe(name, config=config_dict, **position_args)
            
            # Restore stuff here
            # Restore lookup tables for lemmatizer
            if name == "lemmatizer" and 'preserved_lookups' in locals():
                new_component = self._nlp.get_pipe(name)
                new_component.lookups = preserved_lookups
            
            return util.result(f"Successfully modified component '{name}' in pipeline")
        
        except Exception as e:
            return util.error_code(505, f"Error modifying component '{name}': {e}")
        
    # === PIPELINE OUTPUT ===
    def process_text(self, text):
        """
        Process text through the pipeline and return the output in a structured format.
        Outputs as unreadable dict, needs formatting for display.
        """
        try:
            doc = self._nlp(text)
            # Dict for output
            output = {
            "pipeline_components": self._nlp.pipe_names,
            "full_analysis": {}
            }
            
            # Component analysis
            # Transformer
            if "transformer" in self._nlp.pipe_names:
                transformer_info = []
                # Get transformer vectors if available
                if hasattr(doc._, 'trf_data'):
                    vectors = doc._.trf_data.all_outputs[0].data
                    for i in range(min(3, len(doc))):  # First 3 tokens
                        transformer_info.append({
                            # Token text and vector preview
                            "token": doc[i].text,
                            "vector_preview": vectors[i][:10].tolist() if len(vectors[i]) > 10 else vectors[i].tolist()
                        })
                output["full_analysis"]["transformer"] = transformer_info
                
            # Tagger
            if "tagger" in self._nlp.pipe_names:
                tagger_info = []
                for token in doc:
                    if not token.is_space and token.text.strip():
                        tagger_info.append({
                            "text": token.text,
                            "pos": token.pos_,
                            "tag": token.tag_,
                        })
                output["full_analysis"]["tagger"] = tagger_info
                
            # Parser
            if "parser" in self._nlp.pipe_names:
                parser_info = []
                for token in doc:
                    if not token.is_space and token.text.strip():
                        parser_info.append({
                            "text": token.text,
                            "head": token.head.text,
                            "dep": token.dep_,
                            "children": [child.text for child in token.children]
                        })
                output["full_analysis"]["parser"] = parser_info
                
            # Attribute Ruler
            if "attribute_ruler" in self._nlp.pipe_names:
                attribute_ruler_info = []
                for token in doc:
                    if not token.is_space and token.text.strip():
                        attribute_ruler_info.append({
                            "text": token.text,
                            "morph": str(token.morph),
                            "lemma": token.lemma_
                        })
                output["full_analysis"]["attribute_ruler"] = attribute_ruler_info
                
            # Lemmatizer
            if "lemmatizer" in self._nlp.pipe_names:
                lemmatizer_info = []
                for token in doc:
                    if not token.is_space and token.text.strip():
                        lemmatizer_info.append({
                            "text": token.text,
                            "lemma": token.lemma_,
                        })
                output["full_analysis"]["lemmatizer"] = lemmatizer_info
                
            # NER
            if "ner" in self._nlp.pipe_names:
                ner_info = []
                for ent in doc.ents:
                    ner_info.append({
                        "text": ent.text,
                        "label": ent.label_,
                        "start": ent.start,
                        "end": ent.end
                    })
                output["full_analysis"]["ner"] = ner_info
                
            # Full Sentence Breakdown
            sentences_info = []
            sentences = [sent for sent in doc.sents if sent.text.strip()]
            for i, sentence in enumerate(sentences):
                sentence_tokens = []
                for token in sentence:
                    # Ignore spaces and empty tokens
                    if token.is_space or not token.text.strip():
                        continue
                    
                    entity_info = None
                    if token.ent_iob_ != "O": # Is part of an entity
                        entity_info = {
                            "type": token.ent_type_,
                            "iob": token.ent_iob_
                        }
                    
                    sentence_tokens.append({
                        "text": token.text,
                        "pos": token.pos_,
                        "tag": token.tag_,
                        "dep": token.dep_,
                        "head": token.head.text,
                        "lemma": token.lemma_,
                        "morph": str(token.morph),
                        "entity": entity_info
                    })
                
                sentences_info.append({
                    "sentence_number": i + 1,
                    "text": sentence.text.strip(),
                    "tokens": sentence_tokens
                })
            
            output["sentences"] = sentences_info
            return util.result(output)
        except Exception as e:
            return util.error_code(506, f"Error processing text through pipeline: {e}")
        
    def get_component_output(self, text, component_name):
        """Get the output of a specific component for the given text."""
        try:
            if component_name not in self._nlp.pipe_names:
                return util.error_code(507, f"Component '{component_name}' not found in pipeline")
            
            doc = self._nlp(text)
            
            # Handle different components
            # Transformer
            if component_name == "transformer":
                if hasattr(doc._, 'trf_data') and doc._.trf_data is not None:
                    vectors = doc._.trf_data.all_outputs[0].data
                    output = []
                    for i in range(min(3, len(doc))):
                        output.append(f"Token {i} ({doc[i].text}): {vectors[i][:10]}...")
                    return util.result("\n".join(output))
                else:
                    return util.result("No transformer data available")
            # Tagger
            elif component_name == "tagger":
                output = []
                for token in doc:
                    if not token.is_space and token.text.strip():
                        output.append(f"{token.text}: {token.tag_} ({token.pos_})")
                return util.result("\n".join(output))
            # Parser
            elif component_name == "parser":
                output = []
                for token in doc:
                    if not token.is_space and token.text.strip():
                        output.append(f"{token.text}: {token.dep_} -> {token.head.text}")
                return util.result("\n".join(output))
            # Attribute Ruler
            elif component_name == "attribute_ruler":
                output = []
                for token in doc:
                    if not token.is_space and token.text.strip():
                        output.append(f"{token.text}: morph={token.morph}, lemma={token.lemma_}")
                return util.result("\n".join(output))
            # Lemmatizer
            elif component_name == "lemmatizer":
                output = []
                for token in doc:
                    if not token.is_space and token.text.strip():
                        output.append(f"{token.text} -> {token.lemma_}")
                return util.result("\n".join(output))
            # NER
            elif component_name == "ner":
                output = []
                for ent in doc.ents:
                    output.append(f"{ent.text}: {ent.label_} ({ent.start}-{ent.end})")
                return util.result("\n".join(output))
            # Sentencizer
            elif component_name == "sentencizer":
                output = []
                for i, sent in enumerate(doc.sents):
                    output.append(f"Sentence {i+1}: \"{sent.text.strip()}\" (tokens {sent.start}-{sent.end})")
                return util.result("\n".join(output))
            else:
                return util.error_code(508, f"No display made for '{component_name}'")
                
        except Exception as e:
            return util.error_code(509, f"Error getting component output for '{component_name}': {e}")
        
    def format_pipeline_output(self, pipeline_result, show_full_tokens=False):
        """
        Display pipeline output in a readable format.  
        Takes the result from process_text and formats it for display.
        """
        if pipeline_result["error_code"] != 0:
            print("Error in pipeline processing:")
            util.print_error(pipeline_result)
            return
        
        data = pipeline_result["message"]
        
        print("=" * 80)
        print("PIPELINE ANALYSIS RESULTS")
        print("=" * 80)
        
        print(f"\nPipeline Components: {', '.join(data['pipeline_components'])}")
        print(f"Number of Sentences: {len(data['sentences'])}")
        
        # NER Summary
        ner_entities = data['full_analysis']['ner']
        print(f"\nNamed Entities Found: {len(ner_entities)}")
        if ner_entities:
            print("--- NAMED ENTITIES ---")
            for ent in ner_entities:
                print(f"  • {ent['text']}: {ent['label']}")
        
        # Sentence-by-sentence breakdown
        print("\n--- SENTENCE ANALYSIS ---")
        for sentence_data in data['sentences']:
            print(f"\nSentence {sentence_data['sentence_number']}:")
            print(f"  Text: \"{sentence_data['text']}\"")
            print(f"  Tokens: {len(sentence_data['tokens'])}")
            
            if show_full_tokens:
                print("  Token Details:")
                for token in sentence_data['tokens']:
                    entity_info = f" [Entity: {token['entity']['type']}({token['entity']['iob']})]" if token['entity'] else ""
                    print(f"    {token['text']}{entity_info} | POS: {token['pos']} | Tag: {token['tag']} | Dep: {token['dep']} | Head: {token['head']} | Lemma: {token['lemma']}")
            else:
                # Show just entities and key POS tags
                entities = [t for t in sentence_data['tokens'] if t['entity']]
                verbs = [t for t in sentence_data['tokens'] if t['pos'] in ['VERB', 'AUX']]
                nouns = [t for t in sentence_data['tokens'] if t['pos'] in ['NOUN', 'PROPN']]
                
                if entities:
                    entity_list = [f"{t['text']}({t['entity']['type']})" for t in entities]
                    print(f"  Entities: {', '.join(entity_list)}")
                if verbs:
                    verb_list = [f"{t['text']}({t['lemma']})" for t in verbs]
                    print(f"  Verbs: {', '.join(verb_list)}")
                if nouns:
                    noun_list = [f"{t['text']}({t['lemma']})" for t in nouns[:5]]
                    ellipsis = ' ...' if len(nouns) > 5 else ''
                    print(f"  Nouns: {', '.join(noun_list)}{ellipsis}")
        
        print("\n" + "=" * 80)
    
    def get_pipeline_info(self):
        """Get the current pipeline information."""
        return {
            "model_name": self._model_name,
            "components": self._nlp.pipe_names,
            "vocab_size": len(self._nlp.vocab)
        }

# === TESTING ===
if __name__ == "__main__":
    
    run_test_1 = False
    run_test_2 = False
    run_test_3 = False
    run_test_4 = False
    run_test_5 = False
    run_test_6 = True
    
    if run_test_1:
        # Test 1 Blank Pipeline adding spacy component with config
        # Testing with a blank pipeline
        print("Running Test 1: Blank Pipeline adding spacy component with config...")
        pipeline = spacy.blank("en")
        
        interface = PipelineInterface(pipeline)
        print("Pipeline Info:", interface.get_pipeline_info())
        
        # Adding a spacy component
        # Get lemmatizer config from lemmatizer_config.py
        from src.config.lemmatizer_config import config1
        add_result = interface.add_new_spacy_component("lemmatizer", config_dict=config1, position="first")

        print("Add Result:", add_result)
        print("Pipeline components:", interface.get_pipeline_info()["components"])
        
    if run_test_2:
        #Test 2 Modifying existing pipeline component
        print("Running Test 2:  Modifying existing pipeline component...")
        interface = PipelineInterface("en_core_web_trf")
        print("Pipeline Info:", interface.get_pipeline_info())
        
        # Check lemmatizer before modification
        lemmatizer_before = interface._nlp.get_pipe("lemmatizer")
        print("\nPrevious Lemmatizer Settings:")
        print(f"Mode before: {lemmatizer_before.mode}")
        print(f"Overwrite before: {lemmatizer_before.overwrite}")

        # Modifying lemmatizer
        print(f"\nApplying config: {configs.lemmatizer_config.config1}")
        modify_result = interface.modify_spacy_component("lemmatizer", config_dict=configs.lemmatizer_config.config1)
        print("Modify Result:", modify_result)
        
        # Check lemmatizer after modification
        lemmatizer_after = interface._nlp.get_pipe("lemmatizer")
        print("\nNew Lemmatizer Settings:")
        print(f"Mode after: {lemmatizer_after.mode}")
        print(f"Overwrite after: {lemmatizer_after.overwrite}")
        
    if run_test_3:
        # Test 3 single component output
        print("Running Test 3: Single component output...")
        interface = PipelineInterface()
        text = "A fulltime pitch invasion was quickly aborted during the Mid Canterbury club rugby final on Saturday after the referee ruled the game wasn't actually over."
        output = interface.get_component_output(text, "ner")
        print("NER Output:", output["message"])
    
    if run_test_4:
        # Test 4 - Get full pipeline output
        print("Running Test 4: Full pipeline output...")
        interface = PipelineInterface()
        text = "A fulltime pitch invasion was quickly aborted during the Mid Canterbury club rugby final on Saturday after the referee ruled the game wasn't actually over."
        output = interface.process_text(text)
        
        # Displaying full token details
        interface.format_pipeline_output(output, True)
    
    if run_test_5:
        # Test 5 - Removing a component and loading a new custom component with custom function
        print("Running Test 5: Removing a component and loading a new custom component...")
        interface = PipelineInterface()
        # Remove a component
        remove_result = interface.remove_component("tagger")
        print("Remove Result:", remove_result)
        # Add a new custom component
        
        # Define a custom function for the new component
        def custom_component_function(nlp, name):
            """Custom component factory function that returns the actual component."""
            def component(doc):
                print(f"Custom component '{name}' processing: {len(doc)} tokens")
                # Add custom attributes to tokens that will show up in output
                for i, token in enumerate(doc):
                    token.lemma_ = "CHANGED"
                    token.pos_ = "X"
                    token.tag_ = "CHANGED"
                return doc
            return component
        Language.factory("custom_component", func=custom_component_function)
        
        # Add the custom component to the pipeline
        add_result = interface.add_new_custom_component("custom_component", position="first")
        print("Add Custom Component Result:", add_result)
        
        # Process text with the new component
        text = "A fulltime pitch invasion was quickly aborted during the Mid Canterbury club rugby final on Saturday after the referee ruled the game wasn't actually over."
        output = interface.process_text(text)
        # Display the output
        interface.format_pipeline_output(output, True)
        
    if run_test_6:
        # Test 6 - Adding custom component + spacy component
        print("Running Test 6: Adding custom component + sentencizer...")
        interface = PipelineInterface()
        
        # Add a custom component
        def custom_component_function(nlp, name):
            """Custom component that modifies token attributes."""
            def component(doc):
                print(f"Custom component '{name}' processing: {len(doc)} tokens")
                for i, token in enumerate(doc):
                    token.lemma_ = "CHANGED"
                    token.pos_ = "X"
                    token.tag_ = "CHANGED"
                return doc
            return component
        
        Language.factory("custom_component", func=custom_component_function)
        add_custom_result = interface.add_new_custom_component("custom_component", position="first")
        print("Add Custom Component Result:", add_custom_result)
        
        # Add spacy sentencizer component
        try:
            interface._nlp.add_pipe("sentencizer", last=True)
        except Exception as e:
            print(f"Sentencizer failed: {e}")
        
        # Show final pipeline
        print("Final pipeline:", interface.get_pipeline_info()["components"])
        
        # Process text and show results
        text = "This is sentence one. This is sentence two! And this is sentence three?"
        output = interface.process_text(text)
        interface.format_pipeline_output(output, True)
        
        # Test sentencizer component output specifically
        sentencizer_output = interface.get_component_output(text, "sentencizer")
        print("\nSentencizer specific output:")
        print(sentencizer_output["message"])
        
        
        
        