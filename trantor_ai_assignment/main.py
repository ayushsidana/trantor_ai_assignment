from fastapi import FastAPI
from trantor_ai_assignment.openai_app import routes as openai_app_routes
from trantor_ai_assignment.middlewares import setup_middlewares
from trantor_ai_assignment.database import create_db_and_tables

app = FastAPI()

# Setting up middlewares
setup_middlewares(app)

# Include routes from different apps
app.include_router(openai_app_routes.router, prefix="/openai", tags=["openai"])

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()