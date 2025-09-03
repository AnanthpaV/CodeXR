class LLMInterface:
    def __init__(self, model_name):
        self.model_name = model_name

    def send_query(self, query, context_docs=None, debug_mode=False):
        """
        Placeholder LLM call. 
        Replace with OpenAI/Gemini/other API if quota available.
        """
        context_text = f"\nContext: {context_docs}" if context_docs else ""
        mode = "Debug Mode" if debug_mode else "Normal Mode"
        return {
            "response": f"[{self.model_name}] {mode} response for '{query}'{context_text}"
        }

    def receive_response(self, response):
        return response

    def structured_response(self, response, debug_mode=False):
        if debug_mode:
            return {
                "debug": {
                    "error_message": response.get("response"),
                    "explanation": "Likely cause of error",
                    "fix_suggestion": "Suggested fix"
                }
            }
        return {
            "subtasks": ["Step 1: Analyze query", "Step 2: Generate code"],
            "code": "// Example code snippet",
            "gotchas": ["Check API compatibility"],
            "best_practices": ["Use official docs"],
            "difficulty": "Medium",
            "docs_link": "https://docs.unity3d.com/",
            "raw": response
        }
