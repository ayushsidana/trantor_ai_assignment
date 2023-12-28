import backoff
from httpx import AsyncClient
from trantor_ai_assignment.settings import OPENAI_API_KEY

OPENAI_ENDPOINT = "https://api.openai.com/v1/engines/gpt-3.5-turbo/completions"

@backoff.on_exception(backoff.expo, Exception, max_time=60)
async def get_openai_response(question: str) -> str:
    """
    Retrieves a response from the OpenAI GPT-3.5 Turbo engine for a given question.

    This function sends a prompt/question to the OpenAI API and retrieves a response based on it.
    
    Parameters:
    - question (str): The prompt or question for which a response is needed.
    
    Returns:
    - str: The generated text/response from the OpenAI GPT-3.5 Turbo engine based on the provided question.
    
    Raises:
    - Exception: If there's a failure in sending the request to the OpenAI API or retrieving the response.
    """
    async with AsyncClient() as client:
        response = await client.post(
            OPENAI_ENDPOINT,
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            json={"prompt": question, "max_tokens": 150}
        )
        response.raise_for_status()
        return response.json()["choices"][0]["text"].strip()
