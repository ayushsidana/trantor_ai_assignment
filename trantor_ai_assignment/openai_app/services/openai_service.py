import logging
import requests
from trantor_ai_assignment.settings import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_SYSTEM_MESSAGE
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

openai_client = OpenAI(api_key=OPENAI_API_KEY)


class OpenAIRequester:

    def get_requested_data(self, question: str, stream: bool = False) -> requests.Response:
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": OPENAI_SYSTEM_MESSAGE},
                {"role": "user", "content": question}
            ],
            stream=stream,
        )
        return response
