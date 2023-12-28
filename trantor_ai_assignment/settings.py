import environ

# Initialize environ
env = environ.Env()

# Load environment variables from .env file
environ.Env.read_env()

# Access environment variables with default values
DATABASE_URL = env.str('DATABASE_URL')
OPENAI_API_KEY = env.str('OPENAI_API_KEY', default='default_openai_api_key')
CELERY_BROKER_URL = env.str('CELERY_BROKER_URL', default='CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
ALLOWED_ORIGINS = env.str('ALLOWED_ORIGINS', default='*')

print(f"DATABASE_URL: {DATABASE_URL}")
print(f"OPENAI_API_KEY: {OPENAI_API_KEY}")
print(f"CELERY_BROKER_URL: {CELERY_BROKER_URL}")
print(f"CELERY_RESULT_BACKEND: {CELERY_RESULT_BACKEND}")
print(f"ALLOWED_ORIGINS: {ALLOWED_ORIGINS}")
