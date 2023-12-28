import logging
from fastapi import APIRouter, HTTPException
from trantor_ai_assignment.openai_app.services.database_service import fetch_stored_answer
from trantor_ai_assignment.openai_app.services.task_service import wait_and_store_answer
from trantor_ai_assignment.database import get_session
from .schemas import QuestionCreate, QuestionResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()



@router.post("/question/", response_model=QuestionResponse)
async def ask_question(question: QuestionCreate):
    """
    Endpoint to receive a question, check if the answer is stored in the database, 
    and if not, process it asynchronously using Celery.

    Parameters:
    - question (QuestionCreate): The question to be processed.

    Returns:
    - dict: If the answer exists in the database, returns the answer. 
            If not, processes the question asynchronously using Celery.

    Raises:
    - HTTPException: If an internal server error occurs during processing.
    """

    logger.info(f"Received question: {question.question}")

    try:
        with get_session() as db_session:
            # Check if the question exists in the database
            stored_answer = fetch_stored_answer(db_session, question.question)
            if stored_answer:
                return {"answer": stored_answer}

            # If answer doesn't exist in the database, process it asynchronously using Celery
            wait_and_store_answer(db_session, question.question)

            return {"message": "Question received and is being processed."}

    except Exception as e:
        logger.error(f"An error occurred while processing the question: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error occurred.")
