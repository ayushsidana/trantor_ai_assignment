import backoff
import json
import logging
import requests

from trantor_ai_assignment.openai_app.services.database_service import add_question_to_database
from trantor_ai_assignment.openai_app.tasks import generate_openai_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException,), max_time=60, max_tries=5)
def fetch_and_store_openai_answers(question_text):
    """
    Fetches answers from OpenAI based on the provided question text and stores them in the database.

    Args:
        question_text (str): The question for which answers need to be fetched from OpenAI.

    Yields:
        str: The individual answer content retrieved from OpenAI.

    Raises:
        ValueError: If no valid data is yielded from OpenAI.
        requests.exceptions.RequestException: If there's an issue with the request to OpenAI.
        Exception: For any other unexpected errors during processing.

    """
    try:
        answers = []
        streamed_response = generate_openai_response(question=question_text, stream=True)
        for chunk in streamed_response:
            if chunk.choices[0].delta.content is not None:
                answer_content = chunk.choices[0].delta.content
                answers.append(answer_content)
                yield answer_content

        if answers:
            answer = ''.join(answers)
            add_question_to_database(question_text=question_text, answer=answer)
            logger.info(f"Stored answer for question: {question_text}")
        else:
            raise ValueError("No valid data yielded from OpenAI")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from OpenAI: {e}")
        raise
    except Exception as e:
        logger.error(f"Error processing OpenAI answer: {e}")
        raise


def get_streamlined_stored_answer(answer):
    """
    Generator function that breaks down the given 'answer' string into chunks of 10 characters each.
    
    Args:
    - answer (str): The input string that needs to be segmented.
    
    Yields:
    - str: Chunks of 10 characters from the input 'answer' string.
    """
    for chunk in [answer[i:i + 10] for i in range(0, len(answer), 10)]:
        yield chunk


def handle_question(question_text: str):
    """
    Handles the processing of a question text.
    """
    try:
        logger.info(f"Started fetching from OpenAI. {question_text}")
        
        try:
            # Fetch answer from OpenAI
            response = generate_openai_response(question=question_text)
            data_dict = json.loads(response.json())

            # Extract the content
            answer = data_dict['choices'][0]['message']['content'].strip()
        except Exception as openai_error:
            logger.error(f"Error while processing question with OpenAI: {question_text}. Error: {openai_error}")
            raise openai_error
        
        logger.info(f"Storing new answer in the database for question: {question_text}")
        add_question_to_database(question_text, answer)
    
        return answer

    except Exception as error:
        logger.error(f"Error processing question: {question_text}. Error: {error}")
        raise error
