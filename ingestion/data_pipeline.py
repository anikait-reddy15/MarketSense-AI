import os
import json
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

class VectorDatabaseManager:
    def __init__(self, persist_directory: str):
        """Initializes the local embedding model and target database directory."""
        print("[INFO] Initializing HuggingFace Embeddings on CPU...")
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

    def build_vector_store(self, json_files: list[str], collection_name: str = "marketsense_trends", reset: bool = False):
        """Embeds documents and writes them to the local ChromaDB."""
        
        # Reset existing collection contents without destroying the collection entity
        if reset:
            try:
                print(f"[INFO] Clearing existing documents in '{collection_name}'...")
                temp_chroma = Chroma(
                    collection_name=collection_name,
                    persist_directory=self.persist_directory,
                    embedding_function=self.embedding_function
                )
                existing_ids = temp_chroma.get()['ids']
                if existing_ids:
                    temp_chroma.delete(ids=existing_ids)
                    print(f"[INFO] Cleared {len(existing_ids)} stale documents.")
            except Exception as e:
                print(f"[WARNING] Could not clear collection contents: {str(e)}")

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