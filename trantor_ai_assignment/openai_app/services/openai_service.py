import logging
import requests

from trantor_ai_assignment.settings import OPENAI_API_KEY, OPENAI_COMPLETION_ENDPOINT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIRequester:
    def __init__(self, api_key, endpoint):
        self.api_key = api_key
        self.endpoint = endpoint

    def make_request(self, headers, request_data, stream=False):
        response = requests.post(self.endpoint, headers=headers, json=request_data, stream=stream)
        return response


class OpenAIRequester(AIRequester):
    def __init__(self):
        super().__init__(api_key=OPENAI_API_KEY, endpoint=OPENAI_COMPLETION_ENDPOINT)

    def get_requested_data(self, question: str, stream: bool = False) -> requests.Response:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        request_data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ],
            "stream": stream,
        }
        
        return self.make_request(headers=headers, request_data=request_data, stream=stream)
