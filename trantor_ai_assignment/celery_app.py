from celery import Celery

app = Celery("trantor_ai_assignment")
app.config_from_object("trantor_ai_assignment.celery_config")
