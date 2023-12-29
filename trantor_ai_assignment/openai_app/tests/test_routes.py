import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from trantor_ai_assignment.main import app

client = TestClient(app)


class TestQuestionEndpoint(unittest.TestCase):

    @patch('trantor_ai_assignment.openai_app.tasks.handle_question')
    def test_ask_question_non_streaming(self, mock_handle_question):
        mock_handle_question.return_value = "Paris"
        
        response = client.post("/question/non-streaming/", json={"text": "What is the capital of France?"})
        
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("answer", data)
        self.assertEqual(data["answer"], "Paris")

    @patch('trantor_ai_assignment.openai_app.tasks.handle_question')
    def test_ask_question_streaming(self, mock_handle_question):
        mock_handle_question.return_value = "Sunny"
        
        response = client.post("/question/streaming/", json={"text": "What is the weather like today?"})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "Sunny")

    @patch('trantor_ai_assignment.openai_app.tasks.handle_question')
    def test_internal_server_error_non_streaming(self, mock_handle_question):
        mock_handle_question.side_effect = Exception("Mocked internal server error")
            
        response = client.post("/question/non-streaming/", json={"text": "Test question"})
            
        self.assertEqual(response.status_code, 500)
        self.assertIn("Internal Server Error", response.text)

    @patch('trantor_ai_assignment.openai_app.tasks.handle_question')
    def test_internal_server_error_streaming(self, mock_handle_question):
        mock_handle_question.side_effect = Exception("Mocked internal server error")
            
        response = client.post("/question/streaming/", json={"text": "Test question"})
            
        self.assertEqual(response.status_code, 500)
        self.assertIn("Internal Server Error", response.text)
