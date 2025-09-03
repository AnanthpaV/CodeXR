import requests
from bs4 import BeautifulSoup  # pip install beautifulsoup4
from src.rag.rag_retriever import RAGRetriever


class DocsLoader:
    def __init__(self, retriever):
        self.retriever = retriever

    def fetch_and_clean(self, url: str) -> str:
        """Fetch a webpage and clean out HTML/JS/CSS, return plain text."""
        print(f"🌐 Fetching {url} ...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unnecessary tags
        for s in soup(["script", "style", "noscript"]):
            s.extract()

        # Extract visible text
        text = soup.get_text(separator="\n")
        # Shrink whitespace
        text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
        print(f"✅ Cleaned {url} ({len(text)} characters)")
        return text

    def build_index_from_urls(self, urls):
        """Fetch multiple URLs and build RAG index."""
        all_docs = []
        for url in urls:
            try:
                text = self.fetch_and_clean(url)
                all_docs.append(text)
            except Exception as e:
                print(f"⚠️ Failed to fetch {url}: {e}")

        if not all_docs:
            print("❌ No documents fetched. Aborting index build.")
            return

        print("🔧 Building FAISS index from docs...")
        self.retriever.build_index(all_docs)
        print("✅ Index built successfully and stored!")


if __name__ == "__main__":
    print("🚀 Starting docs loader...")

    urls = [
        "https://docs.unity3d.com/Manual/xr_input.html",
        "https://docs.unity3d.com/Manual/xr-interaction-overview.html",
        "https://docs.unrealengine.com/5.0/en-US/virtual-reality-development-in-unreal-engine/",
        "https://docs.unrealengine.com/5.0/en-US/multiplayer-in-unreal-engine/",
        "https://docs.unity3d.com/Manual/SL-Reference.html",
    ]

    retriever = RAGRetriever()  # ✅ Pass retriever into DocsLoader
    loader = DocsLoader(retriever)

    print("🔍 Fetching and indexing docs...")
    loader.build_index_from_urls(urls)
    print("🏁 Docs index built and ready for use!")
