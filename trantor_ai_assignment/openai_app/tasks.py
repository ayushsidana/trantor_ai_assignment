from celery import Celery
from .openai_client import get_openai_response

app = Celery("my_chat_api")
app.config_from_object("celery_config")

@app.task
def process_question(question: str) -> str:
    return get_openai_response(question)