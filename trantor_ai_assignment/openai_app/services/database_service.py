from sqlmodel import Session, select
from ..models import Question

def fetch_stored_answer(db_session: Session, question_text: str) -> str:
    """Fetches a stored answer from the database if it exists."""
    stored_question = db_session.exec(select(Question).where(Question.question == question_text)).first()
    return stored_question.answer if stored_question else None

def add_question_to_database(db_session: Session, question_text: str, answer: str):
    """Adds a new question and its answer to the database."""
    db_question = Question(text=question_text, answer=answer)
    db_session.add(db_question)
    db_session.commit()
