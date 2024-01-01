from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from trantor_ai_assignment.database import create_db_and_tables
from trantor_ai_assignment.middlewares import setup_middlewares
from trantor_ai_assignment.openai_app import routes as openai_app_routes

app = FastAPI()

# Setting up middlewares
setup_middlewares(app)

# Include routes from different apps
app.include_router(openai_app_routes.router, prefix="/openai", tags=["openai"])

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_messages = []
    for error in exc.errors():
        error_messages.append({"field": error.get("loc")[0], "message": error.get("msg")})
    
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error", "errors": error_messages},
    )