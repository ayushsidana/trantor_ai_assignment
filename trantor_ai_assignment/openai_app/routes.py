import logging
from fastapi import APIRouter, HTTPException
from openai_app.services.database_service import fetch_stored_answer, add_question_to_database
from trantor_ai_assignment.database import get_session
from openai_app.schemas import QuestionCreate, QuestionResponse
from openai_app.tasks import process_question

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/question/", response_model=QuestionResponse)
async def ask_question(question: QuestionCreate):
    """
    Receive a question, check if the corresponding answer is available in the database.
    If the answer is found, return it. Otherwise, process the question asynchronously using Celery.
    
    Parameters:
    - question (QuestionCreate): The input question to process.
    
    Returns:
    - QuestionResponse: A response containing the answer or a message indicating the question is being processed.
    
    Raises:
    - HTTPException: If any internal server error occurs during processing.
    """
    logger.info(f"Received question: {question.question}")

    try:
        with get_session() as db_session:
            stored_answer = fetch_stored_answer(db_session, question.question)
            
            if stored_answer:
                return {"answer": stored_answer}
            
            # Process the question asynchronously using Celery
            task = process_question.delay(question.question)
            answer = task.get()
            
            # Store the processed answer in the database
            add_question_to_database(db_session, question.question, answer)
            
            return {"message": "Question received and is being processed asynchronously."}

    except Exception as e:
        logger.error(f"Error occurred while processing the question: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error occurred.")
