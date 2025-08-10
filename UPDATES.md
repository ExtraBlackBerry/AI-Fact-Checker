Documentation on what was worked on

-----26/07/25-----

GOAL: Trying to plan a direction and general idea of how the app should work.

What we did:

    Set up Git repo
    Set up environment on VSCode

    Planned out the app system and direction

        --Core--

        claim extraction
        claim verifier

        --Addtional Features--

        Audio to txt --Add later on
        web browser extension

    Learning more about SpaCy.
    Trying to understand English sentance structures.

    Compressing sentences(Triplet Extraction) using spacy.

------27/07/25------

GOAL: Setting milestones, creating flow chart for each core features.

What we did:

    Worked on the pipeline structure.
    Set up Jira board.

    Made some progress on UML diagram.

------28/07/25------

GOAL: discuss and continue with flow chart and diagrams, start adding features

What we did:

    Decided to add an extra NER layer for more indepth classification of tokens. (updated diagram)
    new diagrams

Feature updates:

    TextCatergorizer custom component - John
    simple wikipedia scraper and sqlite save feature added -John
    pipeline_interface class -Foster

------29/07/25------

GOAL: discussed on the architecture and work on code

What we did:

    Scrapped pipeline interface class and started work on filter 1.
    assigned the architecture for Fact Extraction

Feature updates:

    ClaimFilter1.py custom component - Foster
    added scraper to only get categories with SIMILARITY_RATE similiarty to its title.    // SIMILARITY_RATE can be set in simple_spacy_tool.py -john
    TextCatergorizer now assigns sub_categories from the sqlite db if NER.text exists in the db. -john

-----30/07/25-----

GOAL: Learn more indepth about the filters 1,2 for the extractor

What we did:

    Read more about the rule-based and ML-based classification for fact extraction

Feature updates:

    added diagram on how the ML part of extractor will work -john
    added diagram of rule based extractor -foster
    implemented fallback claimbuster claim extractor -foseter
