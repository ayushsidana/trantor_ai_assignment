from celery import Celery
from services.openai_service import get_openai_response

app = Celery("trantor_ai_assignment")
app.config_from_object("celery_config")

@app.task
def process_question(question: str) -> str:
    return get_openai_response(question)
