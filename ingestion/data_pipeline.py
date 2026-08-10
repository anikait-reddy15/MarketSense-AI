import os
import json
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

class VectorDatabaseManager:
    def __init__(self, persist_directory: str):
        """Initializes the local embedding model and target database directory."""
        print("[INFO] Initializing HuggingFace Embeddings on CPU...")
        
        # FORCED CPU EXECUTION: Prevents PyTorch from locking GPU VRAM
        self.embedding_function = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        self.persist_directory = persist_directory

    def load_json_to_documents(self, filepath: str) -> list[Document]:
        """Reads scraped JSON and converts it into LangChain Document objects."""
        documents = []
        if not os.path.exists(filepath):
            print(f"[WARNING] File not found: {filepath}")
            return documents
            
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for item in data:
            text_content = item.get('text', '')
            title = item.get('title', '')
            url = item.get('url', '')
            source = item.get('source', 'Unknown')
            
            page_content = f"Title: {title}\nContent: {text_content}"
            metadata = {"source": source, "url": url}
            
            doc = Document(page_content=page_content, metadata=metadata)
            documents.append(doc)
            
        return documents

    def build_vector_store(self, json_files: list[str], collection_name: str = "marketsense_trends"):
        """Embeds documents and writes them to the local ChromaDB."""
        all_docs = []
        for file in json_files:
            print(f"[INFO] Processing file: {file}")
            docs = self.load_json_to_documents(file)
            all_docs.extend(docs)
            
        if not all_docs:
            print("[ERROR] No documents loaded. Have you run the scraper yet?")
            return None

        print(f"[INFO] Building ChromaDB vector store with {len(all_docs)} documents...")
        
        vector_store = Chroma.from_documents(
            documents=all_docs,
            embedding=self.embedding_function,
            collection_name=collection_name,
            persist_directory=self.persist_directory
        )
        print(f"[SUCCESS] Vector store successfully built at {self.persist_directory}")
        return vector_store

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(__file__))
    raw_data_dir = os.path.join(base_dir, "data", "raw")
    vector_store_dir = os.path.join(base_dir, "data", "vector_store")
    
    files_to_process = [
        os.path.join(raw_data_dir, "skincare_trends.json"),
        os.path.join(raw_data_dir, "ingredient_trends.json")
    ]
    
    manager = VectorDatabaseManager(persist_directory=vector_store_dir)
    manager.build_vector_store(files_to_process)