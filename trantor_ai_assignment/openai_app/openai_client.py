import backoff
from httpx import AsyncClient
from trantor_ai_assignment.settings import OPENAI_API_KEY

OPENAI_ENDPOINT = "https://api.openai.com/v1/engines/gpt-3.5-turbo/completions"

@backoff.on_exception(backoff.expo, Exception, max_time=60)
async def get_openai_response(question: str) -> str:
    async with AsyncClient() as client:
        response = await client.post(
            OPENAI_ENDPOINT,
            headers={"Authorization": f"Bearer sfsag"},
            json={"prompt": question, "max_tokens": 150}
        )
        response.raise_for_status()
        return response.json()["choices"][0]["text"].strip()
