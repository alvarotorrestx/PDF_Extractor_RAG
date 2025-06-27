# PDF Extractor - Retrieval‑Augmented Generation (RAG) system


## Reflection Report


### Description of PDF: [Outline Plan for Leprechaun Animation Implementation](Outline%20Plan%20for%20Leprechaun%20Animation%20Implementation.pdf)


The PDF is an outline plan that I created as a "take-home" exam for a job interview for position of "E-Commerce Developer." The PDF outlines variations of methods on how a "jumping" Leprechaun can appear on the website screen randomly and would offer a discount/free gift upon the user "catching" it.

---

### Five deep‑dive questions & AI answers


**1\. What does the embedding dimensionality represent, and why must it match the FAISS index’s expected input size?**

Understanding this ensures that your question vectors and document vectors are compatible for meaningful similarity comparisons.


**2\. How does FAISS determine similarity when using IndexFlatL2, and how does that affect retrieval accuracy?**

This reveals how vector distances are calculated (L2 = Euclidean) and helps you reason about which chunks are considered “close” or relevant.


**3\. How does chunk size and chunk overlap impact the quality of context retrieval and the completeness of answers?**

Choosing too small a chunk may miss context; too large, and it may dilute relevance. Overlap helps with continuity between adjacent chunks.


**4\. How should the prompt be structured to ensure the generator gives grounded and context-aware responses?**

Prompt quality directly influences how well the generator uses the provided context. It's key for preventing hallucinations.


**5\. What are the limitations of using a small model like flan-t5-small in terms of reasoning depth and factual consistency?**

Model size impacts performance. Knowing this helps you balance speed vs. accuracy and decide when to upgrade.

---

### Analysis of:

**How retrieval quality varied with different chunk_size and chunk_overlap**

When I used smaller chunks, the system gave more detailed pieces of the document but sometimes lost the overall idea. Larger chunks gave broader context but sometimes included too much info. In between them all with the 500/50 chunks seemed to give the best balance between focus and context.


**Quality of generated responses**


The responses were technically and generally close to the answer I was expecting, just with a lot of extra context. The system would just copy parts of the document instead of answering more directly. Giving keywords and asking short questions helped get a clearer response.


**Suggestions for improvements or extensions**


To make the results even better, perhaps using a bigger AI model might also help it understand questions more clearly. Maybe even adding chat history could help improve the AI itself.