from groq import Groq

from .config import get_api_key


MODEL = "openai/gpt-oss-20b"


class ModuxAI:

    def __init__(self):

        api_key = get_api_key()

        if not api_key:
            raise RuntimeError(
                "Modux has not been configured with a Groq API key."
            )

        self.client = Groq(
            api_key=api_key
        )

    def chat(
        self,
        system_prompt,
        user_prompt,
    ):

        response = self.client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return response.choices[0].message.content.strip()