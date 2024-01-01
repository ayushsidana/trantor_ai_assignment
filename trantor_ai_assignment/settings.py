import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables with default values
DATABASE_URL = os.getenv('DATABASE_URL', default='default_database_url')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', default='default_openai_api_key')
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', default='*')

OPENAI_MODEL = "gpt-3.5-turbo"

OPENAI_SYSTEM_MESSAGE = "You are a helpful assistant."
