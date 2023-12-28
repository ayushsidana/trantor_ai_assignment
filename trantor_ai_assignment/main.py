from fastapi import FastAPI
from trantor_ai_assignment.openai_app import routes as openai_app_routes
from trantor_ai_assignment.middlewares import setup_middlewares

app = FastAPI()

# Setting up middlewares
setup_middlewares(app)

from fastapi import FastAPI
from trantor_ai_assignment.openai_app import routes as openai_app_routes

# Include routes from different apps
app.include_router(openai_app_routes.router, prefix="/openai", tags=["App1"])
