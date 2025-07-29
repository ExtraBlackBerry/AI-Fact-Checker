import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.classes.pipeline_interface import PipelineInterface
import src.config as configs
import spacy
from spacy.language import Language 
    
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