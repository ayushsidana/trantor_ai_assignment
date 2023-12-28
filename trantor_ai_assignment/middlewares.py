from trantor_ai_assignment.settings import ALLOWED_ORIGINS
from fastapi.middleware.cors import CORSMiddleware

def setup_middlewares(app):
    origins = ALLOWED_ORIGINS.split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
