import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from trantor_ai_assignment.openai_app.routes import router

client = TestClient(router)


class ChatEndpointTests(unittest.TestCase):

    def test_ask_question_success(self):
        response = client.post("/chat", json={"text": "What is the capital of France?"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["text"], "What is the capital of France?")
        self.assertIn("answer", response.json())

    def test_ask_question_failure(self):
        response = client.post("/chat", json={})
        self.assertEqual(response.status_code, 500)

class StreamChatEndpointTests(unittest.TestCase):

    @patch('your_fastapi_main_module.fetch_stored_answer')
    def test_stream_chat_with_stored_answer(self, mock_fetch_stored_answer):
        mock_fetch_stored_answer.return_value = ["StoredAnswerChunk"]
        response = client.post("/stream-chat", json={"text": "What is the capital of France?"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")

        chunks = list(response.iter_lines())
        expected_chunks = ["StoredAnswerChunk"]
        self.assertEqual(chunks, expected_chunks)

    @patch('your_fastapi_main_module.fetch_and_store_openai_answers')
    def test_stream_chat_without_stored_answer(self, mock_fetch_and_store_openai_answers):
        mock_fetch_and_store_openai_answers.return_value = ["FirstChunk", "SecondChunk", "ThirdChunk"]
        
        response = client.post("/stream-chat", json={"text": "What is the capital of Spain?"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")

        chunks = list(response.iter_lines())
        expected_chunks = ["FirstChunk", "SecondChunk", "ThirdChunk"]
        self.assertEqual(chunks, expected_chunks)

    def test_stream_chat_failure(self):
        response = client.post("/stream-chat", json={})
        self.assertEqual(response.status_code, 500)
