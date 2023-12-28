from trantor_ai_assignment.celery_app import app
from trantor_ai_assignment.openai_app.services.openai_service import get_openai_response

@app.task
def process_question(question: str) -> str:
    return get_openai_response(question)
