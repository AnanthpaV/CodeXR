from llm.llm_interface import LLMInterface

class DebugHandler:
    def __init__(self, model_name="GPT-4o-mini"):
        self.known_errors = {
            "NullReferenceException": "This happens when a required component is not assigned. Fix: Assign the missing reference in the Inspector or via script.",
            "Blueprint runtime error": "This occurs when a node has invalid inputs. Fix: Check your Blueprint node connections.",
        }
        self.llm = LLMInterface(model_name)

    def analyze_error(self, error_log, context_docs=None):
        error_log = error_log.strip()

        # 1. Check against known patterns
        for key, suggestion in self.known_errors.items():
            if key.lower() in error_log.lower():
                return {
                    "error_message": error_log,
                    "explanation": f"Detected known issue: {key}",
                    "fix_suggestion": suggestion,
                }

        # 2. Fallback: Ask LLM
        llm_response = self.llm.send_query(
            f"Explain this error log and suggest a fix:\n{error_log}",
            context_docs=context_docs,
            debug_mode=True,
        )
        structured = self.llm.structured_response(llm_response, debug_mode=True)

        return structured["debug"]
