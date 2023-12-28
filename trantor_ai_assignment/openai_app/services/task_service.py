from sqlmodel import Session
from ..models import Question
from ..tasks import process_question
from fastapi import HTTPException
from .database_service import add_question_to_database
import logging

logger = logging.getLogger(__name__)

def wait_and_store_answer(db_session: Session, question_text: str):
    try:
        # Enqueue the question for processing using Celery
        task = process_question.delay(question_text)
        
        # Retrieve the answer from the Celery task result
        answer = task.get()
        
        # Store the question and answer in the database using the database_service function
        add_question_to_database(db_session, question_text, answer)

        # Log successful storage of the answer
        logger.info(f"Stored answer for question: {question_text}")
    
    except (ValueError, TypeError) as ve:
        # Catch specific exceptions related to value or type errors
        logger.error(f"Value or Type error occurred while storing the answer for question '{question_text}': {str(ve)}")
        raise HTTPException(status_code=400, detail="Bad request data.")
    
    except Exception as e:
        # Catch any other general exceptions
        logger.error(f"An error occurred while storing the answer for question '{question_text}': {str(e)}")
        raise HTTPException(status_code=500, detail="Error storing the answer.")
