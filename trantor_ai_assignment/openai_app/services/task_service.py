import logging
from fastapi import HTTPException
from sqlmodel import Session

from openai_app.tasks import process_question
from openai_app.services.database_service import add_question_to_database

logger = logging.getLogger(__name__)

def wait_and_store_answer(db_session: Session, question_text: str):
    """
    Enqueues a question for processing using Celery, waits for the processed answer, 
    and then stores the question-answer pair in the database.
    
    Parameters:
    - db_session (Session): The active database session to store the question-answer pair.
    - question_text (str): The text of the question to be processed and stored.
    
    Raises:
    - HTTPException: If there's a value or type error, a 400 status code is raised with a "Bad request data" detail.
    """
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
        logger.error(f"Value or Type error occurred while storing the answer for question '{question_text}': {str(ve)}")
        raise HTTPException(status_code=400, detail="Bad request data.")
    
    except Exception as e:
        # Catch any other general exceptions
        logger.error(f"An error occurred while storing the answer for question '{question_text}': {str(e)}")
        raise HTTPException(status_code=500, detail="Error storing the answer.")
