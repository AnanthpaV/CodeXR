from fastapi import FastAPI, Body
from llm.llm_interface import LLMInterface
from web_search.search import WebSearch
from structured_output.output_formatter import OutputFormatter
from rag.rag_retriever import RAGRetriever
from debugging.debug_handler import DebugHandler

app = FastAPI()

SERPAPI_API_KEY = "aa67d4ff97ad83b7f8ddb6e94457829c89d8131382b9f24e918310ca9d048691"

llm = LLMInterface("GPT-4o-mini")
search = WebSearch(SERPAPI_API_KEY)
formatter = OutputFormatter()
retriever = RAGRetriever()
debugger = DebugHandler()

@app.post("/query")
def query(user_query: str = Body(...), error_logs: str = Body(default="")):
    if error_logs:
        debug_result = debugger.analyze_error(error_logs)
        llm_response = llm.send_query(error_logs, debug_mode=True)
        structured = llm.structured_response(llm_response, debug_mode=True)
        result = formatter.format(structured, debug_data=debug_result)
    else:
        context_docs = retriever.retrieve(user_query)
        llm_response = llm.send_query(user_query, context_docs=context_docs)
        structured = llm.structured_response(llm_response)
        search_results = search.perform_search(user_query)
        result = formatter.format(structured, search_results=search_results, retrieved_docs=context_docs)

    # ✅ Ensure snippet is always present
    if "snippet" not in result:
        result["snippet"] = structured.get("code_snippet", "") or "print('No snippet generated')"

    return result
