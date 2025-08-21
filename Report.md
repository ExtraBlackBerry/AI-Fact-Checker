#

#

#

#

# Report

Version 2.8.2bs

6th August, 2025

FAVS(FAct Verification System)

[John Yoo](https://www.linkedin.com/in/shunjyoo/)  
[Foster Rae](https://www.linkedin.com/in/fosterrae/)

[\[Github\]](https://github.com/ExtraBlackBerry/PBT-FactCheckerApp)

#

# Abstract

In the modern digital era, the rapid spread of misinformation poses a threat to public knowledge. This project addresses the challenge of verifying factual claims found online. This project is focused on the development of a functional prototype, FAVS (FAct Verification System), an AI-powered tool designed to analyze and verify factual claims. The system utilizes a custom Natural Language Processing (NLP) pipeline to extract check worthy claims from text, retrieve evidence from external knowledge bases, and deliver a score for the claim along with sources of evidence. The final deliverable is a browser extension that allows users to verify the validity of any claims in a selected text through the right click context menu.

#

# Introduction and Background

The field of Artificial Intelligence, particularly Natural Language Processing (NLP), has revolutionized how we interact with and process textual and spoken information. From translation to voice assistants, NLP allows machines to understand, interpret, and generate human language. This project uses NLP techniques to tackle the critical issue of online misinformation, a problem extensively documented as the modern ‘infodemic’ (Van Der Linden, 2022\) [\[1\]](https://www.nature.com/articles/s41591-022-01713-6).

##

## Objectives

The primary objectives of this project were to:

- Implement valid claim extraction from browser text.
- Implement key information extraction from an identified claim.
- Develop an intuitive user interface.
- Build a backend FastAPI server connecting to the browser extension.

##

## characteristics/features

The system was designed with several key features.

- **Browser Integration**: Operates as a simple to install browser extension, allowing integration with a user’s daily browsing habits.
- **Context-Menu Activation**: The primary user interaction is designed to be intuitive and efficient. A user can simply highlight any text on a webpage, right click, and select the ‘Fact Check’ option from the context menu to start an analysis.
- **Real Time Feedback**: Aims to provide verification for small text in near real time (target of under 5 seconds).
- **NLP Core**: The system is run by a backend built on the spaCy library, utilizing a pre-trained transformer model ‘en_core_web_trf’ for high accuracy linguistic analysis, including Named Entity Recognition (NER) and Part-of-Speech (POS) tagging.

## Need

With the explosion of information sharing via the internet,the roles of traditional editors and professional fact checkers have been largely bypassed. This has led to an environment where false information and malicious propaganda can spread rapidly. There is a need for tools that empower individuals to assess the validity of the information they encounter daily.

The significance of FAVS lies in its potential to act as a first line of defense against misinformation for the general public. By providing an easy to use tool that integrates directly into the web browser, the project aims to promote media literacy and encourage a more critical consumption of online content, hopefully mitigating the impacts of false information.

#

# Methodology

##

## Problem domain

The project operates within the problem domain of automated fact checking. The specific focus is on extracting factual claims from a given text and returning a score for each claim found.

Our development follows a rapid iterative prototyping approach with a ‘core-out’ strategy, focusing first on the central NLP engine. Then adding extras like tidying up the input and output of the system later.

The system was implemented as a multi stage pipeline:

- **Claim Extraction**: Identify claims in a text.
- **Information Extraction**: Key information is isolated from the claim.
- **Evidence Retrieval**: APIs are queried with this information.
- **Claim Scoring**: The user is given supporting evidence and a score for the claim.

##

## Tools/AI Techniques

The implementation of this project relies on the following software and AI techniques:

- **Backend**:
  - **Language**: Python 3.10.11
  - **Framework**: FastAPI
- **Frontend:** JavaScript
- **Database:** SQLite.
- **APIs:** Google Programmable Search Engine, Duckduckgo, Wikipedia
- **Operating System**: Development and testing were conducted on Windows.
- **Libraries:**
  - spaCy, scikit-learn, matplotlib, seaborn

##

## Project architecture

The user interacts with the system via the browser extension. This can be done by right clicking highlighted text and selecting the ‘Fact Check’ option. The text is then sent to the backend and enters the NLP pipeline. If a claim is found, external APIs are queried with the key information in these claims and a score is given based on the evidence the APIs return. This score along with links to the evidence are sent to the browser extension to be displayed to the user.

1. **Claim Extraction**: This phase uses a two-stage filtering system to extract factual claims. First, a submitted text is processed by a spaCy pipeline that uses a pre-trained model for POS tagging and NER. The text is then passed to a rule-based filter, which uses the linguistic features given by the spaCy pipeline to identify and extract claims. Any remaining text is analyzed by an SVM classifier trained on the ClaimBuster Dataset. The rule-based filter is designed to target more specific claim types, while the SVM acts as a catch all to identify claims that fall outside of the predefined rules.  

2. **Information Extraction**: Once a claim is extracted, the system pulls out its core components to build an effective search query. It extracts key entities using NER and the grammatical subjects of the claim (via ‘nsubj’ dependency parsing). These components are then structured into search prompts.  

3. **Evidence Gathering**: The constructed queries are sent to the Google Search API to retrieve a list of relevant web pages. For each result, the system collects the page title and its summary snippet. A similarity check is then performed between the original claim and each title/summary pair. Only results that exceed a predefined threshold are retained, creating a filtered list of potential evidence.

4. **Claim Scoring**: Each piece of potential evidence is scored against the original claim using a pre-trained model from the Hugging Face library. This model outputs a label showing if the evidence supports the claim. The similarity score for each piece of potential evidence calculated in the previous step is multiplied by the label, then averaged to get the final score.

5. **Interface Display**: The final score along with supporting evidence is sent to the extension to be displayed to the user in a clean, intuitive manner.

## Time frame Estimation of each phase

![][image1]

#

# Results and Evaluation

The extraction process was evaluated on a previously unseen test validation set by Claimbusters. After integrating both filter1 (Rule-Based) and filter2(SVM) into the extraction pipeline, the resulting performance demonstrated a remarkable improvement when compared to baseline models available publicly.

Model 1 was configured with a filter 1 threshold of 8, which resulted in higher predictive accuracy but a lower F1 score. This behaviour is expected, since a stricter threshold leads to more precise extraction by rejecting borderline cases, which reduces recall. In contrast, Model 2 applied a lower filter 1 threshold of 4, allowing a larger number of claims (including some faulty ones) to pass through, increasing recall at the expense of precision.  
Filter2 recovered approximately 80 % of the claims missed by filter1 and achieved an accuracy of around 93 %. Overall, both iterations of our proposed models outperformed the existing baseline models across all evaluated metrics.

Since factual claims are continuously updated and new evidence may emerge that supports both positive and negative outcomes, it is difficult to establish a definitive ground-truth for verification. Consequently, we adopted an alternative method of evaluation based on user testing.

To evaluate the effectiveness of our verification pipeline, we defined the following settings:

- **Summary Similarity** – cosine similarity between the claim and the summary of the website returned from the Google API.  

- **Title Similarity** – cosine similarity between the claim and the title of the website returned from the Google API.  

- **Separate Claims** – whether each claim was searched individually or sent collectively in a single query.  

- **Forced Entity** – whether the returned result is required to contain the entities extracted using spaCy.  

- **Sort by Relevance** – whether the results returned from the Google API are sorted based on relevance.

We performed five separate testing sessions, each with a distinct group of participants.  
Each group consisted of a mixture of both tech-savvy and non-tech-savvy users.  
For all testing sessions, the same verification pipeline settings described above were used.

| GROUPS  | Summary Similarity | Title Similarity | Separate Claims | Forced Entity | Sort by Relevence | Result                                                                                                                      |
| :------ | :----------------- | :--------------- | :-------------- | :------------ | :---------------- | :-------------------------------------------------------------------------------------------------------------------------- |
| GROUP 1 | 30%                | 10%              | TRUE            | TRUE          | FALSE             | Links provided were very slightly relevant to the topic, Score given had very small variance. USER FEEDBACK:OVERALL MIXED   |
| GROUP 2 | 20%                | 0%               | TRUE            | TRUE          | FALSE             | Links provided were very slightly relevant to the topic, Score given had very small variance.USER FEEDBACK:OVERALL NEGATIVE |
| GROUP 3 | 20%                | 10%              | FALSE           | FALSE         | FALSE             | Links provided were little relevant to the topic, Score given had good varianceUSER FEEDBACK:OVERALL MIXED                  |
| GROUP 4 | 20%                | 0%               | FALSE           | FALSE         | FALSE             | Links provided were relevant to the topic, score given had wide range of variance.USER FEEDBACK:OVERALL POSITIVE            |
| GROUP 5 | 20%                | 0%               | FALSE           | FALSE         | TRUE              | Links provided were relevant to the claim, score given had wide range of variance.USER FEEDBACK: OVERALL POSITIVE            |

Title Similarity had a negative impact on the verifier’s output. Applying a high similarity threshold substantially limited the amount of evidence that could be retrieved, which in turn lowered the overall verification scores. In most cases, the webpage titles were only loosely related, or even unrelated, to the actual content, which resulted in very low similarity scores. Disabling the title similarity check (i.e., setting the threshold to 0 %) significantly improved our ability to retrieve relevant sources.

Summary Similarity proved useful for filtering out completely irrelevant search results. Therefore, we retained the check, but used a relatively low threshold—high enough to exclude sources with no relevance, but low enough to avoid discarding potentially useful evidence.

Separate Claims produced worse results. Sending individual claims in separate queries reduced the overall context available to the search engine and consistently resulted in less relevant evidence. Combining all claims in a single query led to more coherent and relevant results.

Forced Entity exhibited a similar issue to the title similarity check. Requiring retrieved results to explicitly contain the extracted entities filtered out a large proportion of relevant sources, and thus negatively impacted overall performance.

Sort by Relevance, enabled using the Google API’s built-in ranking, consistently improved performance by prioritising the collection of relevant evidence.

Overall, our model’s extraction pipeline demonstrated strong performance and consistently outperformed the online baseline models. In contrast, the verifier still requires further experimentation and refinement, particularly in the areas of search prompt generation and threshold tuning, to improve its ability to gather reliable and consistent evidence.

After installing the extension in the browser via Chrome's developer mode, executing the main.py file starts the FastAPI server. Once the backend server is running, the user can invoke the extension by right-clicking and selecting the “Fact Check” option. The selected text is then transmitted to the backend API, which processes the request and returns a fact-checking score together with links to any supporting or refuting evidence. The extension interface is subsequently updated to display these results to the user.

##

## Limitations

The primary limitation lies in the complexity of fully automated verification. The difficulty of programmatically determining trustworthy sources for any given claim is a large challenge that leads most professional fact-checking organizations to rely on human experts.

Furthermore, the only available training datasets are often specialized (e.g., political speech), which reduces claim extraction effectiveness for more general topics.

Another limitation is that the reliance on public search APIs introduces inconsistency due to variable response quality and rate limiting. Moreover, the performance of the verifier heavily depends on the structure and specificity of the generated search queries.

Finally, the absence of a definitive ground-truth for the retrieved evidence limits the ability to train and evaluate the verifier in a fully supervised manner.

# Discussion and Conclusions

To conclude, this project produced a functional prototype of the Fact Verification System.

Our key technical achievement was the validation of our two-filter extraction component. The results show that combining a rigid rule-based filter with a flexible SVM safety net is a highly effective approach that outperforms standard publicly available models.

User evaluations of the pipeline revealed several important insights:

- The choice of thresholds in the claim extraction stage has a significant impact on performance. Higher thresholds improve precision but reduce recall.  

- The evidence retrieval strategy plays an important role in determining the relevance and usefulness of the results. Enforcing strict entity or title similarity requirements reduced the overall verification performance. In contrast, a lower summary similarity threshold and enabling relevance-based ranking of results via the Google API, improved both the quality of the retrieved evidence and the usefulness of the returned score.  

- The user interface and integration with the browser context menu was effective in providing an accessible and seamless user experience. Non-technical users were still able to interact with the extension and understand the output.

This project also identifies a few key areas for future development:  


- A primary limitation of the current claim extractor is its reliance on the ClaimBuster dataset which is specialized in political speech. Future iterations would involve training the SVM classifier on a more generalized dataset, should one become available, or combining multiple domain-specific datasets to improve the extractors effectiveness across a wider range of content.  

- To enhance the verification component, the system could be integrated with APIs from established fact-checking organizations. Accessing these databases of pre-verified claims would allow the system to quickly match an extracted claim against the known truth, providing users with a definitive and trustworthy verdict.  

- The current system relies on standard search engine results. Future work would focus on more sophisticated retrieval methods, such as utilizing vector-based search across a curated set of reliable sources or querying knowledge graphs like wikidata. Furthermore, a source reliability model could be developed to assess the trustworthiness of evidence, assigning higher weights to established news organizations or academic institutions and lower weights to unverified or biased sources.

While the complexities of automated fact-checking remain a challenge, this project provides a robust framework and clear path forward for developing more advanced and reliable verification tools.

[image1]: data:image/png;base64,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
