from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from config import Config

class VectorStore:
    def __init__(self):
        self.local_database = "local_database"
        self.embedding = HuggingFaceEmbeddings(model_name = Config.EMBEDDING_MODEL)
    
    def save_embedding(self, chunks):
        """Save vector embeddings for document chunks using FAISS."""
        db = FAISS.from_documents(chunks, self.embedding)
        db.save_local(self.local_database)
        print("DB Saved")
    
    def similarity_search(self, query):
        """ Retrieve similar chunks from the local database """
        db = FAISS.load_local(self.local_database, self.embedding, allow_dangerous_deserialization=True)
        similar_chunks = db.similarity_search(query = query, k=6)
        return similar_chunks
