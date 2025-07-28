# 28.07.25 Foster
# Interface to manipulate the spacy pipeline and view results
import spacy

class PipelineInterface:
    """Interface for managing and analyzing a Spacy NLP pipeline."""
    
    def __init__(self, model_name="en_core_web_trf"):
        self.model_name = model_name # Default to "en_core_web_trf"
        self.nlp = spacy.load(model_name)
        # Dicts to keep track of custom components and extensions
        self.custom_components = {}
        self.custom_extensions = {}
    
    # === COMPONENT MANAGEMENT ===

    def add_custom_component(self):
        """Add a custom component to the pipeline."""
        pass
    
    def remove_custom_component(self):
        """Remove a custom component from the pipeline."""
        pass

    def reorder_components(self):
        """Reorder components in the pipeline."""
        pass
        
    def list_components(self):
        """List all components in the pipeline."""
        return self.nlp.pipe_names
    
    # === NER MANAGEMENT ===
    
    def add_entity_label(self):
        """Add a new entity label to the NER component."""
        pass
    
    def remove_entity_label(self):
        """Remove an entity label from the NER component."""
        pass
    
    def list_entity_labels(self):
        """List all entity labels in the NER component."""
        pass
    
    # === ENTITY RULER MANAGEMENT ===
    
    def add_entity_patterns(self):
        """Add a new pattern to the entity ruler."""
        pass
    
    def remove_entity_patterns(self):
        """Remove a pattern from the entity ruler."""
    
    def list_entity_patterns(self):
        """List all entity ruler patterns."""
        pass
    
    # === EXTENSION MANAGEMENT ===
    
    def add_token_extension(self):
        """Add custom token extension."""
        pass
    
    def add_span_extension(self):
        """Add custom span extension."""
        pass
    
    def add_doc_extension(self):
        """Add custom document extension."""
        pass
    
    def remove_extension(self):
        """Remove custom extension."""
        pass
    
    def list_extensions(self):
        """List all custom extensions."""
        pass
    
    # === PIPELINE UTILITIES ===
    
    def get_pipeline_info(self):
        """Get the current pipeline information."""
        return {
            "model_name": self.model_name,
            "components": self.nlp.pipe_names,
            "custom_components": list(self.custom_components.keys()),
            "custom_extensions": list(self.custom_extensions.keys()),
            "entity_labels": self.list_entity_labels(),
            "vocab_size": len(self.nlp.vocab)
        }
    
    # === TEXT PROCESSING ===
    def process_text(self, text):
        """Process text and return structured output."""
        pass
    
    def print_component_output(self, component_name):
        """Print the output from a specific component."""
        pass
    

# === TESTING ===
if __name__ == "__main__":
    
    pipeline = PipelineInterface()
    
    # Print pipeline info
    print(pipeline.get_pipeline_info())
    
    # List components
    print("Pipeline Components:", pipeline.list_components())