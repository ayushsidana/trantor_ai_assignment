from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from trantor_ai_assignment.main import app
from trantor_ai_assignment.database import get_session

client = TestClient(app)

@patch('trantor_ai_assignment.database.get_session')
def test_ask_question_new_question(mock_get_session):
    mock_session = MagicMock()
    mock_session.exec.return_value.first.return_value = None
    mock_get_session.return_value = mock_session

    response = client.post("openai/question/", json={"question": "What is FastAPI?"})
    assert response.status_code == 200
    assert response.json() == {"message": "Question received and is being processed."}

@patch('trantor_ai_assignment.database.get_session')
def test_ask_question_existing_question(mock_get_session):
    mock_session = MagicMock()
    mock_session.exec.return_value.first.return_value = {"answer": "FastAPI is a modern web framework for building APIs."}
    mock_get_session.return_value = mock_session

    response = client.post("openai/question/", json={"question": "What is FastAPI?"})
    assert response.status_code == 200
    assert response.json() == {"answer": "FastAPI is a modern web framework for building APIs."}

@patch('trantor_ai_assignment.database.get_session')
def test_ask_question_error(mock_get_session):
    mock_get_session.side_effect = Exception("Database connection error")

    response = client.post("openai/question/", json={"question": "What is FastAPI?"})
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error occurred."}
