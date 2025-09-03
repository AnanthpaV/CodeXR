import os
from dotenv import load_dotenv

from rag.rag_retriever import RAGRetriever
from debugging.debug_handler import DebugHandler

# Load API key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def test_rag():
    print("\n=== Testing RAG Retriever ===")
    retriever = RAGRetriever(api_key=OPENAI_API_KEY)

    # Example: pretend we indexed docs
    docs = """
    In Unity XR Toolkit, the TeleportationProvider is required for teleport locomotion.
    You must assign it in the XR Rig or via script before using teleportation features.
    """
    retriever.build_index(docs)

    query = "How do I add teleport locomotion in Unity VR?"
    results = retriever.retrieve(query, k=2)
    print("Query:", query)
    print("Retrieved Docs:", results)

def test_debugging():
    print("\n=== Testing Debugging Mode ===")
    debugger = DebugHandler()

    # Known error
    error1 = "NullReferenceException: TeleportationProvider not set"
    result1 = debugger.analyze_error(error1)
    print("Error Log:", error1)
    print("Debug Result:", result1)

    # Unknown error (should fallback to LLM)
    error2 = "Shader compilation failed: unexpected token"
    result2 = debugger.analyze_error(error2)
    print("\nError Log:", error2)
    print("Debug Result:", result2)

if __name__ == "__main__":
    test_rag()
    test_debugging()
