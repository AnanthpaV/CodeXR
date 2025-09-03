def validate_input(input_data):
    # Validate the input data for correctness
    if not isinstance(input_data, str) or not input_data.strip():
        raise ValueError("Input must be a non-empty string.")
    return input_data.strip()

def handle_error(error):
    # Handle errors and return a user-friendly message
    return {"error": str(error)}

def format_response(response):
    # Format the response from the LLM or web search
    if isinstance(response, dict):
        return response
    return {"message": response}