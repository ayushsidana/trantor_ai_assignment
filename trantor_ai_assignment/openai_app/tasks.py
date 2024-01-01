import logging
from trantor_ai_assignment.celery_app import app
from trantor_ai_assignment.openai_app.services.openai_service import OpenAIRequester

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.task
def generate_openai_response(question, stream=False):
    """
    Generate a response from OpenAI based on the given question.
    
    Args:
        question (str): The question to send to OpenAI.
        stream (bool, optional): Whether to stream the response or not. Defaults to False.
        
    Returns:
        str: OpenAI's response.
        
    Raises:
        Exception: If an error occurs while generating the OpenAI response.
    """
    try:
        openai_requester = OpenAIRequester()
        response = openai_requester.get_requested_data(question, stream=stream)
        return response
    except Exception as exc:
        error_message = f"Error occurred while generating OpenAI response for question '{question}': {str(exc)}"
        logger.error(error_message)
        raise exc
