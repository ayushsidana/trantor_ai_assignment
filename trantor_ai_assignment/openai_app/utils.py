import backoff
import json
import logging
import requests

from trantor_ai_assignment.openai_app.services.database_service import add_question_to_database
from trantor_ai_assignment.openai_app.services.openai_service import OpenAIRequester

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
        openai_requester = OpenAIRequester()
        response = openai_requester.get_requested_data(question=question_text, stream=True)
        response.raise_for_status()

        for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
            for line in chunk.split('\n'):
                if line.startswith('data: '):
                    try:
                        json_data = json.loads(line[6:])
                        choices = json_data.get("choices")
                        if choices and choices[0].get("delta"):
                            answer_content = choices[0]["delta"]["content"]
                            answers.append(answer_content)
                            yield answer_content
                    except json.JSONDecodeError as e:
                        logger.warning(f"JSON decode error encountered: {e}")
                        continue

        if answers:
            add_question_to_database(question_text=question_text, answer=''.join(answers))
            logger.info(f"Stored answer for question: {question_text}")
        else:
            raise ValueError("No valid data yielded from OpenAI")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from OpenAI: {e}")
        raise
    except Exception as e:
        logger.error(f"Error processing OpenAI answer: {e}")
        raise
