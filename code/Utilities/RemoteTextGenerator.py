import os
import openai

from typing import Optional
from dataclasses import dataclass

@dataclass(slots = True)
class RemoteTextGenerator:

    """
    A remote random text generator that
    uses the help of OpenAI, to create
    random text.

    :param model: The default model name.
    :param temperature: The default sampling temperature.
    :param default_length: The default target character length.
    """

    model = "gpt-4o-mini"
    temperature = 0.8
    default_length = 256

    def generate(
        self,
        char_length: Optional[int] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> Optional[str]:

        """
        Generates - if possible - a creative text via OpenAI.

        :param char_length: The approximate target length in characters.
        :param model: The optional gpt model to override the default.
        :param temperature: The optional temperature to override the default.
        :return: The processed generated text from the API.
        """

        requested = max(16, int(char_length or self.default_length))
        gpt_model = model or self.model
        chosen_temp = self.temperature if temperature is None else temperature

        api_key = os.getenv("OPENAI_API_KEY") or getattr(openai, "api_key", None)
        if not api_key: return None

        max_tokens = max(16, int(requested / 3.5) + 20)
        system_prompt = (
            "You are an assistant that returns a single short creative text fragment. "
            "Produce one paragraph of imaginative text, roughly the requested length. "
            "No lists or code, just plain text."
        )
        user_prompt = f"Please write a random text of about {requested} characters."

        try:

            client = openai.OpenAI(api_key = api_key)
            resp = client.chat.completions.create(
                model = gpt_model,
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens = max_tokens,
                temperature = chosen_temp,
                n = 1,
            )
            content = (resp.choices[0].message.content or "").strip()
        except Exception: content = None

        return content[:requested] if content else None
