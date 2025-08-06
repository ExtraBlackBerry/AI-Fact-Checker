# 06.08.25 John

if __debug__:
    import sys
    import os

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.classes.extractorAI import ExtractorAI



if __name__ == "__main__":
    model = ExtractorAI("Datasets/text2doc.spacy")
    model.test_cluster(100)