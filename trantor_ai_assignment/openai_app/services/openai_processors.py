import json
import logging
import requests
import backoff

from trantor_ai_assignment.openai_app.services.database_service import add_question_to_database
from trantor_ai_assignment.openai_app.tasks import generate_openai_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIProcessor:
    def __init__(self, question_text):
        self.question_text = question_text

    def fetch_and_store_openai_answers(self):
        raise NotImplementedError

    def store_answer_to_database(self, answer):
        """
        Common method to store the answer to the database.
        """
        try:
            add_question_to_database(question_text=self.question_text, answer=answer)
            logger.info(f"Stored answer for question: {self.question_text}")
        except Exception as error:
            logger.error(f"Error storing answer to the database: {error}")
            raise


class StreamedOpenAIProcessor(OpenAIProcessor):
    @backoff.on_exception(backoff.expo, (requests.exceptions.RequestException,), max_time=60, max_tries=5)
    def fetch_and_store_openai_answers(self):
        try:
            answers = []
            streamed_response = generate_openai_response(question=self.question_text, stream=True)
            for chunk in streamed_response:
                if chunk.choices[0].delta.content is not None:
                    answer_content = chunk.choices[0].delta.content
                    answers.append(answer_content)
                    yield answer_content

            if answers:
                answer = ''.join(answers)
                self.store_answer_to_database(answer)
            else:
                raise ValueError("No valid data yielded from OpenAI")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from OpenAI: {e}")
            raise
        except Exception as e:
            logger.error(f"Error processing OpenAI answer: {e}")
            raise


class DirectOpenAIProcessor(OpenAIProcessor):
    def fetch_and_store_openai_answers(self):
        try:
            response = generate_openai_response(question=self.question_text)
            data_dict = json.loads(response.json())
            answer = data_dict['choices'][0]['message']['content'].strip()

            self.store_answer_to_database(answer)

            return answer

        except Exception as error:
            logger.error(f"Error processing question: {self.question_text}. Error: {error}")
            raise
