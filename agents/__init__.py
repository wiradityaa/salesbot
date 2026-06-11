from .intent_classifier import classify_intent
from .tool_router import route
from .response_generator import generate_response

# -------------------------------------------------------
# Main pipeline — entry point untuk UI
# -------------------------------------------------------

def run_pipeline(user_query: str) -> dict:
    """
    Full pipeline: query → intent → tool → response.
    Return dict dengan keys: answer, intent_data, raw_data.
    """
    # Step 1: Classify intent
    intent_result = classify_intent(user_query)
    intent_data   = intent_result.get("data", {})

    # Step 2: Route ke tool yang sesuai
    analytics_data = route(intent_data)

    # Step 3: Generate response
    answer = generate_response(
        user_query=user_query,
        analytics_data=analytics_data,
        intent_data=intent_data
    )

    return {
        "answer":      answer,
        "intent_data": intent_data,
        "raw_data":    analytics_data
    }