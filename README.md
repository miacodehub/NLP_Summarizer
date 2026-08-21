**NLP based text summarizer**

# Problem statement

As a software engineer, when working on a feature, I often refer to existing documentation surrounding the product to save time on my research and problem resolution. While official documentation is a great guide, usually the best insights come from personal notes or files saved by developers over the years. These personal notes contain information related to developers' experience, what they've tried, what worked or didn't, and what the limitations were at the time of resolution.

A key problem I face while searching within these documents is that they're hardly ever in the same format. Searching a specific keyword or issue in different forms of text documents is difficult and time consuming. Also, while pdf allows for multi-file search, word and notepad files offer limited such functionality.

# Solution 

When RAG systems became prevalent, I realized a RAG based text summarizer that searched different documents and enabled summarization across different documents could be a great tool to improve team productivity. Moreover, depending on the retrieval and generation models used, the tool can generate better results the more it is used.

This project is a lighter version of a similar idea. It's objective is to take the query provided by the user and search the documents for information regarding the query and return a summary based on the relevant results found in the documents.

So far, this application supports documents of types .docx, .txt, and .pdf. 

# Architecture
<img width="837" height="1240" alt="arc_new" src="https://github.com/user-attachments/assets/85b87b6e-f91d-497a-9f4b-df0a3a73e689" />

# Output

## With  single format of a file
## With all 3 formats
## When info is not present in the files



# Evaluation of the model
Evaluation focused on verifying that the system could retrieve relevant document content and generate answers grounded in that content.

A small set of manually created question-answer pairs was used to test the pipeline across different document sections.

The evaluation checked:

Retrieval relevance: whether the correct document chunks were retrieved for a given query.
Similarity scores: whether relevant queries produced higher semantic similarity scores.
Answer correctness: whether the generated answer was supported by the retrieved context.
End-to-end behavior: document upload → retrieval → answer generation.

The system also exposes the retrieval similarity score with each response, making it possible to inspect whether an answer was generated from sufficiently relevant context.

Note: This is a prototype evaluation rather than a statistically rigorous benchmark. A larger labeled dataset and automated metrics would be required for a formal evaluation.

## Improvements

While building the first version of the product, I've noticed that my application was generating incorrect answers. 

For the embeddings, I was using the BGE small model. It creates 384 dimension embeddings and is specifically towards retrieval.

While I thought about changing the model, its published MTEB results show a 51.68 retrieval score, versus 49.04 for e5-small-v2 and 43.81 for all-mpnet-base-v2; more importantly, BGE explicitly positions the model family for retrieval and recommends its rerankers for improving retrieval quality.

For summarization, I used the FLAN-T5 model since it's a simple model that can be used for summarizations and other NLP use cases.
However, most of the incorrectness of my application comes from this model.

### Model distillation for improving generated summary

BEFORE:

The first version of my tool used a FLAN T5 Small model for generation of a summary from retrieved contexts.
The summary generated wasn't always accurate most of the time, as can be seen below:
<img width="1198" height="795" alt="image" src="https://github.com/user-attachments/assets/6b33013a-06cd-4557-b5d7-532042120266" />

So I made a few improvements to improve with the quality of answers.




# Limitations of the model

Since this is a personal project, I used smaller models for retrieval and generation. 

Also, the documents used are primarily text based. This may pose as a limitation when there's documents with images and tables or other pictorial representation of data present.

The following are the limitations in detail:

**Small evaluation dataset:**
The current evaluation uses a limited number of manually created questions and does not provide statistically significant performance measurements.

**Generation quality:** FLAN-T5-small is lightweight but can produce inaccurate or poorly grounded answers, particularly when the retrieved context is ambiguous or insufficient.

**Retrieval sensitivity:** Performance depends on chunk size, embedding quality, and the similarity threshold used for retrieval.

**Limited context handling:** Only a small number of retrieved chunks are passed to the generation model, which can cause relevant information to be missed.

**No reranking:**  Retrieved chunks are selected directly using FAISS similarity search without a dedicated reranking model.

**No hallucination detection:** The system does not independently verify whether the generated answer is fully supported by the source document.

**Limited document complexity:** The current ingestion pipeline primarily handles extracted text and may perform poorly with tables, images, scanned documents, or complex layouts.

**Model scale:** The models were intentionally kept relatively small for local execution, which limits answer quality compared with larger instruction-tuned LLMs.
