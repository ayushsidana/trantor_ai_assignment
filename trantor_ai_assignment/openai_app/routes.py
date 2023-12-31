import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from trantor_ai_assignment.openai_app.schemas import QuestionCreate, QuestionResponse
from trantor_ai_assignment.openai_app.services.database_service import fetch_stored_answer
from trantor_ai_assignment.openai_app.utils import fetch_and_store_openai_answers
from trantor_ai_assignment.openai_app.tasks import handle_question

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat", response_model=QuestionResponse)
async def ask_question(question: QuestionCreate):
    try:
        logger.info(f"Received question: {question.text}")
        question_text = question.text

        answer = fetch_stored_answer(question_text)
        if not answer:
            answer = await handle_question(question_text)

        return QuestionResponse(text=question_text, answer=answer)

    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_stored_answer(answer):
    for chunk in [answer[i:i + 10] for i in range(0, len(answer), 10)]:
        yield chunk


@router.post('/stream-chat')
def stream_chat(question: QuestionCreate):
    try:
        question_text = question.text
        logger.info(f"Received question: {question_text}")

        answer = fetch_stored_answer(question_text)
        if answer:
            logger.info(f"Answer found in database for question: {question_text}")
            return StreamingResponse(get_stored_answer(answer), media_type="application/json")
        else:
            logger.info(f"Fetching answer from OpenAI for question: {question_text}")
            return StreamingResponse(fetch_and_store_openai_answers(question_text), media_type="application/json")

    except Exception as e:
        logger.error(f"Error streaming answer: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
