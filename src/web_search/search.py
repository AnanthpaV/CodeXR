from langchain_community.utilities import SerpAPIWrapper

class WebSearch:
    def __init__(self, api_key):
        self.search = SerpAPIWrapper(serpapi_api_key=api_key)

    def perform_search(self, query):
        try:
            result = self.search.run(query)
            return {"search_result": result}
        except Exception as e:
            return {"search_result": f"Error: {str(e)}"}