import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from trantor_ai_assignment.main import app

client = TestClient(app)


class TestQuestionEndpoint(unittest.TestCase):

    @patch('trantor_ai_assignment.openai_app.services.database_service.fetch_stored_answer')
    def test_get_answer_from_database(self, mock_fetch_stored_answer):
        mock_fetch_stored_answer.return_value = "Paris"
        
        response = client.post("openai/question/", json={"text": "What is the capital of France?"})
        
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("answer", data)
        self.assertEqual(data["answer"], "Paris")

    @patch('trantor_ai_assignment.openai_app.tasks.process_question')
    def test_process_question_asynchronously(self, mock_process_question):
        mock_process_question.return_value = "Sunny"
        
        response = client.post("openai/question/", json={"text": "What is the weather like today?"})
        
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("answer", data)
        self.assertEqual(data["answer"], "Sunny")

    @patch('trantor_ai_assignment.openai_app.services.database_service.fetch_stored_answer')
    def test_internal_server_error(self, mock_fetch_stored_answer):
        mock_fetch_stored_answer.side_effect = Exception("Mocked internal server error")
            
        response = client.post("openai/question/", json={"text": "Test question"})
            
        self.assertEqual(response.status_code, 500)
        self.assertIn("Internal server error occurred.", response.text)
