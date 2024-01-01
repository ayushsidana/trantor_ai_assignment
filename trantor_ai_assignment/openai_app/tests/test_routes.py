import unittest
from unittest.mock import patch
from trantor_ai_assignment.main import app
from trantor_ai_assignment.openai_app.utils import get_streamlined_stored_answer

from fastapi.testclient import TestClient

client = TestClient(app)


class TestChatEndpoint(unittest.TestCase):
    @patch('trantor_ai_assignment.openai_app.routes.handle_question')
    def test_ask_question_success(self, mock_handle_question):
        # Set the return value of the mocked function by awaiting the coroutine
        mock_handle_question.return_value = "FastAPI is a modern, fast web framework for building APIs."
        
        # Make the API request
        response = client.post("/openai/chat", json={"text": "What is FastAPI?"})
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTrue("text" in response.json())
        self.assertTrue("answer" in response.json())
        self.assertEqual(response.json()["text"], "What is FastAPI?")
        self.assertEqual(response.json()["answer"], "FastAPI is a modern, fast web framework for building APIs.")

    def test_ask_question_validation_error(self):
        # Test validation error due to missing 'text' field
        response = client.post("openai/chat", json={})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {
            "detail": "Validation error",
            "errors": [
                {
                    "field": "body",
                    "message": "field required"
                }
            ]
        })

        # Test validation error due to invalid 'text' length
        response = client.post("openai/chat", json={"text": "Short"})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {
            "detail": "Validation error",
            "errors": [
                {
                    "field": "body",
                    "message": "Question length must be between 10 and 500 characters."
                }
            ]
        })

        # Test validation error due to 'text' containing spam content
        response = client.post("openai/chat", json={"text": "Is this spam content?"})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {
            "detail": "Validation error",
            "errors": [
                {
                    "field": "body",
                    "message": "Spam content is not allowed in questions."
                }
            ]
        })

    def test_ask_question_internal_server_error(self):
        # Test fetch_stored_answer exception
        with patch('trantor_ai_assignment.openai_app.routes.fetch_stored_answer') as mock_fetch_stored_answer:
            mock_fetch_stored_answer.side_effect = Exception("Mocked error")
            
            response = client.post("/openai/chat", json={"text": "Mocked question"})
            
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json(), {"detail": "Internal Server Error"})

        # Test handle_question exception
        with patch('trantor_ai_assignment.openai_app.routes.handle_question') as mock_handle_question:
            mock_handle_question.side_effect = Exception("Mocked error")
            
            response = client.post("/openai/chat", json={"text": "Mocked question"})
            
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json(), {"detail": "Internal Server Error"})

class TestStreamChatEndpoint(unittest.TestCase):

    @patch('trantor_ai_assignment.openai_app.routes.fetch_stored_answer')
    def test_stream_chat_with_stored_answer_success(self, mock_fetch_stored_answer):
        mock_fetch_stored_answer.return_value = "Stored answer for FastAPI."
        
        response = client.post("/openai/stream-chat", json={"text": "What is FastAPI?"})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")
        self.assertEqual(response.text, "Stored answer for FastAPI.")

    @patch('trantor_ai_assignment.openai_app.routes.fetch_and_store_openai_answers')
    def test_stream_chat_with_openai_success(self, mock_fetch_and_store_openai_answers):
        # Mock the function to return a StreamingResponse.
        mocked_answer = "OpenAI answer for FastAPI."
        mock_fetch_and_store_openai_answers.return_value = get_streamlined_stored_answer(mocked_answer)
        
        response = client.post("/openai/stream-chat", json={"text": "What is FastAPI?"})
        
        # For instance, the status_code might not be 200 if it's streaming.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")
        
        # Check if the returned content matches your expectation.
        self.assertEqual(response.content.decode('utf-8'), mocked_answer)


    def test_stream_chat_validation_error(self):
        # Test validation error due to missing 'text' field
        response = client.post("/openai/stream-chat", json={})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {
            "detail": "Validation error",
            "errors": [
                {
                    "field": "body",
                    "message": "field required"
                }
            ]
        })

        # Test validation error due to invalid 'text' length
        response = client.post("/openai/stream-chat", json={"text": "Short"})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {
            "detail": "Validation error",
            "errors": [
                {
                    "field": "body",
                    "message": "Question length must be between 10 and 500 characters."
                }
            ]
        })

        # Test validation error due to 'text' containing spam content
        response = client.post("/openai/stream-chat", json={"text": "Is this spam content?"})
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {
            "detail": "Validation error",
            "errors": [
                {
                    "field": "body",
                    "message": "Spam content is not allowed in questions."
                }
            ]
        })

    def test_stream_chat_internal_server_error(self):
        # Test fetch_stored_answer exception
        with patch('trantor_ai_assignment.openai_app.routes.fetch_stored_answer') as mock_fetch_stored_answer:
            mock_fetch_stored_answer.side_effect = Exception("Mocked error")
            
            response = client.post("/openai/stream-chat", json={"text": "Mocked question"})
            
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json(), {"detail": "Internal Server Error"})

        # Test fetch_and_store_openai_answers exception
        with patch('trantor_ai_assignment.openai_app.routes.fetch_and_store_openai_answers') as mock_fetch_and_store_openai_answers:
            mock_fetch_and_store_openai_answers.side_effect = Exception("Mocked error")
            
            response = client.post("/openai/stream-chat", json={"text": "Mocked question"})
            
            self.assertEqual(response.status_code, 500)
            self.assertEqual(response.json(), {"detail": "Internal Server Error"})