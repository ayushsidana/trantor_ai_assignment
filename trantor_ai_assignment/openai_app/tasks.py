import logging
from trantor_ai_assignment.celery_app import app
from trantor_ai_assignment.openai_app.services.openai_service import OpenAIRequester

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.task
def generate_openai_response(question, stream=False):
    try:
        openai_requester = OpenAIRequester()
        response = openai_requester.get_requested_data(question, stream=stream)
        return response
    except Exception as e:
        return str(e)
