from sqlmodel import select
from ..models import Question
from trantor_ai_assignment.database import get_session


def fetch_stored_answer(question_text: str) -> str:
    """
    Fetches a stored answer associated with the provided question text from the database.
    
    Parameters:
    - question_text (str): The text of the question for which the stored answer is to be retrieved.
    
    Returns:
    - str: The stored answer corresponding to the provided question text if it exists in the database. 
           Returns None if no answer is found for the given question text.
    """
    with get_session() as db_session:
        stored_question = db_session.exec(select(Question).where(Question.text == question_text)).first()
        return stored_question.answer if stored_question else None


def add_question_to_database(question_text: str, answer: str):
    """
    Adds a new question and its answer to the database.
    
    Parameters:
    - question_text (str): The text of the question to be added.
    - answer (str): The answer corresponding to the question.
    """
    with get_session() as db_session:
        db_question = Question(text=question_text, answer=answer)
        db_session.add(db_question)
        db_session.commit()
