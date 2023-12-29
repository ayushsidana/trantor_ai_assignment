import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from trantor_ai_assignment.openai_app.schemas import QuestionCreate, QuestionResponse
from trantor_ai_assignment.openai_app.tasks import handle_question

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/question/non-streaming/", response_model=QuestionResponse)
async def ask_question_non_streaming(question: QuestionCreate):
    """
    Handle a question asynchronously and provide a non-streaming response.

    This endpoint receives a question, processes it asynchronously using the 
    handle_question task, and returns a non-streaming response containing the 
    question text and the generated answer.

    Args:
        question (QuestionCreate): The input question with text.

    Returns:
        QuestionResponse: A response containing the original question text and 
                          the generated answer.

    Raises:
        HTTPException: If there's an internal server error during processing.
    """
    try:
        logger.info(f"Received question for non-streaming: {question.text}")
        answer = await handle_question(question.text)
        return QuestionResponse(text=question.text, answer=answer)
    except Exception as e:
        logger.error(f"Error processing non-streaming question: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/question/streaming/")
async def ask_question_streaming(question: QuestionCreate):
    """
    Stream the response for the given question.

    This endpoint receives a question, processes it asynchronously using the 
    handle_question task, and streams the generated answer as a text/plain 
    streaming response.

    Args:
        question (QuestionCreate): The input question with text.

    Returns:
        StreamingResponse: A streaming response containing the generated answer.

    Raises:
        HTTPException: If there's an internal server error during processing.
    """
    try:
        logger.info(f"Received question for streaming: {question.text}")

        async def generate():
            answer = handle_question(question.text)
            yield answer

        return StreamingResponse(generate(), media_type="text/plain")
    except Exception as e:
        logger.error(f"Error processing streaming question: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
