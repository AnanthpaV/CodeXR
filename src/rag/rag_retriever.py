from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

class RAGRetriever:
    def __init__(self, index_path="data/faiss_index"):
        self.index_path = index_path
        # ✅ Force CPU for embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"}   # <<< This is the fix
        )
        self.db = None

    def build_index(self, docs):
        print("🔨 Splitting text into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        splits = []
        for d in docs:
            splits.extend(text_splitter.split_text(d))

        print(f"📑 Split into {len(splits)} chunks.")
        self.db = FAISS.from_texts(splits, self.embeddings)

        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        self.db.save_local(self.index_path)
        print(f"💾 Index saved at {self.index_path}")
        print("✅ Index built successfully and stored!")

    def load_index(self):
        if os.path.exists(self.index_path):
            self.db = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)
            print(f"✅ Loaded FAISS index from {self.index_path}")
        else:
            print("⚠️ No FAISS index found. Run docs_loader first.")

    def retrieve(self, query):
        if not self.db:
            self.load_index()
        if not self.db:
            return ["⚠️ No index found. Run build_index() or docs_loader first."]
        docs = self.db.similarity_search(query, k=3)
        return [d.page_content for d in docs]
