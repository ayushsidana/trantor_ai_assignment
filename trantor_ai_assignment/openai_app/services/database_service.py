from sqlmodel import Session, select
from ..models import Question

def fetch_stored_answer(db_session: Session, question_text: str) -> str:
    """
    Fetches a stored answer associated with the provided question text from the database.
    
    Parameters:
    - db_session (Session): The active database session to perform the query.
    - question_text (str): The text of the question for which the stored answer is to be retrieved.
    
    Returns:
    - str: The stored answer corresponding to the provided question text if it exists in the database. 
           Returns None if no answer is found for the given question text.
    """
    stored_question = db_session.exec(select(Question).where(Question.question == question_text)).first()
    return stored_question.answer if stored_question else None


def add_question_to_database(db_session: Session, question_text: str, answer: str):
    """
    Adds a new question and its answer to the database.
    
    Parameters:
    - db_session (Session): The database session object.
    - question_text (str): The text of the question to be added.
    - answer (str): The answer corresponding to the question.
    """
    db_question = Question(text=question_text, answer=answer)
    db_session.add(db_question)
    db_session.commit()
