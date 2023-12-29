import logging

from fastapi import APIRouter, HTTPException
from trantor_ai_assignment.openai_app.services.database_service import fetch_stored_answer, add_question_to_database
from trantor_ai_assignment.database import get_session
from trantor_ai_assignment.openai_app.schemas import QuestionCreate, QuestionResponse
from trantor_ai_assignment.openai_app.tasks import process_question

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
    logger.info(f"Received question: {question.text}")
    question_text = question.text

    try:
        with get_session() as db_session:
            stored_answer = fetch_stored_answer(db_session, question_text)
            
            if stored_answer:
                return QuestionResponse(text=question_text, answer=stored_answer)
            
            # Process the question asynchronously using Celery
            answer = await process_question(question_text)
            
            # Store the processed answer in the database
            add_question_to_database(db_session, question_text, answer)
            
            return QuestionResponse(text=question_text, answer=answer)

    except Exception as e:
        logger.error(f"Error occurred while processing the question: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error occurred.")
