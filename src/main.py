import os
import streamlit as st
from llm.llm_interface import LLMInterface
from web_search.search import WebSearch
from structured_output.output_formatter import OutputFormatter
from rag.rag_retriever import RAGRetriever
from debugging.debug_handler import DebugHandler
from speech.whisper_handler import WhisperHandler   # NEW

SERPAPI_API_KEY = "aa67d4ff97ad83b7f8ddb6e94457829c89d8131382b9f24e918310ca9d048691"

def main():
    st.title("CodeXR: AI-Powered Coding Assistant for AR/VR Developers")

    # --- Sidebar ---
    st.sidebar.header("User Input")
    user_query = st.sidebar.text_area("Enter your coding query:")
    error_logs = st.sidebar.text_area("Paste error logs (optional):")
    
    model_name = st.sidebar.selectbox("Choose LLM Model", ["Gemini-2.5", "GPT-4o-mini", "StarCoder2"])

    # --- Whisper Speech-to-Text ---
    st.sidebar.header("🎤 Voice Input (Optional)")
    audio_file = st.sidebar.file_uploader("Upload voice query (WAV only)", type=["wav"])
    if audio_file:
        whisper_handler = WhisperHandler(model_name="base")
        try:
            user_query = whisper_handler.transcribe(audio_file)
            st.sidebar.success(f"Transcribed Query: {user_query}")
        except Exception as e:
            st.sidebar.error(f"Whisper error: {e}")


    # --- Initialize components ---
    llm = LLMInterface(model_name)
    search = WebSearch(SERPAPI_API_KEY)
    formatter = OutputFormatter()
    retriever = RAGRetriever()
    debugger = DebugHandler()

    # Show retriever status
    if retriever.db:
        st.sidebar.success("✅ Docs index loaded")
    else:
        st.sidebar.warning("⚠️ No docs index found. Run `python -m utils.docs_loader` first.")

    # --- Handle Submit ---
    if st.sidebar.button("Submit"):
        if not (user_query or error_logs):
            st.warning("Please enter a query or error logs (or upload audio).")
            return

        if error_logs:
            debug_result = debugger.analyze_error(error_logs)
            llm_response = llm.send_query(error_logs, debug_mode=True)
            structured = llm.structured_response(llm_response, debug_mode=True)
            final_output = formatter.format(structured, debug_data=debug_result)

        else:
            context_docs = retriever.retrieve(user_query)
            llm_response = llm.send_query(user_query, context_docs=context_docs)
            structured = llm.structured_response(llm_response)
            search_results = search.perform_search(user_query)
            final_output = formatter.format(
                structured,
                search_results=search_results,
                retrieved_docs=context_docs
            )

        # --- Display Results ---
        st.subheader("💡 Assistant Response")
        st.json(final_output)

        # Show docs preview in a nicer way
        if final_output.get("retrieved_docs"):
            st.subheader("📚 Retrieved Docs")
            for i, doc in enumerate(final_output["retrieved_docs"], start=1):
                st.markdown(f"**Doc {i} Preview**\n\n{doc[:1000]}...\n")

if __name__ == "__main__":
    main()

