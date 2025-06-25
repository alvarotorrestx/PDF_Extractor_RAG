# ----- Logging and Warning Configuration -----
import logging
import warnings
from transformers import logging as hf_logging, pipeline
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss


# Set logging level for langchain and transformers
logging.getLogger("langchain.text_splitter").setLevel(logging.ERROR)
hf_logging.set_verbosity_error()

# Suppress all Python warnings
warnings.filterwarnings("ignore")


# ----- RAG Configuration Variables -----
chunk_size = 500
chunk_overlap = 50
model_name = "sentence-transformers/all-distilroberta-v1"
top_k = 5


# ----- Load Extracted Text -----
text = ""
try:
    with open("Selected_Document.txt", "r", encoding="utf-8") as f:
        text = f.read()
    print("📄 Document loaded into memory.")
except Exception as e:
    print(f"❌ Failed to read 'Selected_Document.txt': {e}")


# ----- Split Text into Chunks -----
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    separators=['\n\n', '\n', ' ', '']
)

chunks = text_splitter.split_text(text)
print(f"🧩 Split into {len(chunks)} chunks.")


# ----- Encode Chunks and Create FAISS Index -----
# Load the embedding model
model = SentenceTransformer(model_name)

# Encode the text chunks into embeddings (suppress progress bar)
embeddings = model.encode(chunks, show_progress_bar=False)

# Convert to NumPy float32 array
embedding_array = np.array(embeddings).astype("float32")

# Initialize FAISS index with the correct dimension
dimension = embedding_array.shape[1]
index = faiss.IndexFlatL2(dimension)

# Add embeddings to the index
index.add(embedding_array)

print(f"📦 Indexed {len(chunks)} chunks into FAISS (dim={dimension}).")


# ----- Set Up Text Generation Pipeline -----
# Initialize the text-to-text generation pipeline using CPU
generator = pipeline(
    task='text2text-generation',
    model='google/flan-t5-small',
    device=-1  # -1 indicates CPU; change to 0 for GPU
)

print("🧠 Text generation pipeline is ready.")


# ----- Define Retrieval and Answering Functions -----
def retrieve_chunks(question, k=top_k):
    """
    Encodes the question, searches FAISS, and returns the top-k most similar text chunks.
    """
    question_embedding = model.encode([question], show_progress_bar=False).astype("float32")
    distances, indices = index.search(question_embedding, k)
    return [chunks[i] for i in indices[0] if i < len(chunks)]

def answer_question(question):
    """
    Retrieves relevant chunks, constructs a prompt with context, and generates an answer.
    """
    relevant_chunks = retrieve_chunks(question)
    context = "\n".join(relevant_chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    
    response = generator(prompt, max_new_tokens=200, do_sample=False)
    generated_text = response[0]['generated_text']
    return generated_text


if __name__ == "__main__":
    print("Enter 'exit' or 'quit' to end.")
    while True:
        question = input("Your question: ")
        if question.lower() in ("exit", "quit"):
            print("👋 Goodbye!")
            break
        answer = answer_question(question)
        print("🧠 Answer:", answer)
