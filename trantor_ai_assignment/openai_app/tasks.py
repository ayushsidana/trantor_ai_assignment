import logging
from trantor_ai_assignment.celery_app import app
from trantor_ai_assignment.openai_app.services.database_service import add_question_to_database
from trantor_ai_assignment.openai_app.services.openai_service import OpenAIRequester
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.task
async def handle_question(question_text: str):
    """
    Asynchronously handles the processing of a question text.
    """
    try:
        logger.info(f"Started fetching from OpenAI. {question_text}")
        
        try:
            # Fetch answer from OpenAI
            openai_requester = OpenAIRequester()
            response = openai_requester.get_requested_data(question=question_text)
            response.raise_for_status()
            answer = response.json()["choices"][0]["message"]["content"].strip()
        except Exception as openai_error:
            logger.error(f"Error while processing question with OpenAI: {question_text}. Error: {openai_error}")
            raise openai_error
        
        logger.info(f"Storing new answer in the database for question: {question_text}")
        add_question_to_database(question_text, answer)
    
        return answer

    except Exception as error:
        logger.error(f"Error processing question: {question_text}. Error: {error}")
        raise error
