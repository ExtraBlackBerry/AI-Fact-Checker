# 28.07.25 Foster
# Interface to manipulate the spacy pipeline and view results
if __debug__:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import spacy
from src.util import util

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
        
        