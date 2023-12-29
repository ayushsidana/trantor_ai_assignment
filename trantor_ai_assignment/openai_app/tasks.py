import logging
from trantor_ai_assignment.celery_app import app
from trantor_ai_assignment.openai_app.services.openai_service import get_openai_response
from trantor_ai_assignment.openai_app.services.database_service import fetch_stored_answer, add_question_to_database
from trantor_ai_assignment.database import get_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.task
async def handle_question(question_text: str):
    """
    Asynchronously handles the processing of a question text.

    This task function processes a given question text by first checking 
    if a pre-stored answer exists in the database. If no pre-stored answer 
    is found, it invokes the OpenAI API to generate a new answer. Once 
    the answer is obtained, it is stored in the database for future use.

    Args:
        question_text (str): The question text to be processed.

    Returns:
        str: The generated answer for the provided question text.

    Raises:
        Exception: If there's an error during database operations, while 
                   fetching the OpenAI response, or any other unexpected errors.
    """
    try:
        with get_session() as db_session:
            stored_answer = fetch_stored_answer(db_session, question_text)
            
            if stored_answer:
                logger.info(f"Found stored answer for question: {question_text}")
                return stored_answer

            logger.info(f"No stored answer found for question: {question_text}. Fetching from OpenAI.")
            
            try:
                # Fetch answer from OpenAI
                answer = await get_openai_response(question_text)
            except Exception as openai_error:
                logger.error(f"Error while processing question with OpenAI: {question_text}. Error: {openai_error}")
                raise openai_error
            
            # Store the new answer in the database
            logger.info(f"Storing new answer in the database for question: {question_text}")
            add_question_to_database(db_session, question_text, answer)
            
            return answer

    except Exception as error:
        logger.error(f"Error processing question: {question_text}. Error: {error}")
        raise error
