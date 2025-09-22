import os
import openai

from dataclasses import dataclass
from typing import Optional

@dataclass(slots=True)
class RemoteTextGenerator:
    """
    Remote text generator using OpenAI Chat Completions.

    :param model: Default model name.
    :param temperature: Default sampling temperature.
    :param default_length: Default target character length.
    """
    model: str = "gpt-4o-mini"
    temperature: float = 0.9
    default_length: int = 256

    def generate(
        self,
        length_chars: Optional[int] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> Optional[str]:
        """
        Try generating creative text via OpenAI. Returns None on error or missing key.

        :param length_chars: Approximate target length in characters.
        :param model: Optional model override.
        :param temperature: Optional temperature override.
        :return: Text trimmed to requested length, or None on failure.
        """
        requested = max(16, int(length_chars or self.default_length))
        chosen_model = model or self.model
        chosen_temp = float(self.temperature if temperature is None else temperature)

        api_key: Optional[str] = os.getenv("OPENAI_API_KEY") or getattr(openai, "api_key", None)
        if not api_key:
            return None

        max_tokens = max(16, int(requested / 3.5) + 20)
        system_prompt = (
            "You are an assistant that returns a single short creative text fragment. "
            "Produce one paragraph of imaginative text, roughly the requested length. "
            "No lists or code, just plain text."
        )
        user_prompt = f"Please write a random text of about {requested} characters."

        # Primary: modern client (openai>=1.x)
        try:
            client = openai.OpenAI(api_key=api_key)  # type: ignore[attr-defined]
            resp = client.chat.completions.create(
                model=chosen_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=max_tokens,
                temperature=chosen_temp,
                n=1,
            )
            content = (resp.choices[0].message.content or "").strip()
        except Exception:
            content = None

        if content:
            return content[:requested]

        # Fallback: legacy API (openai<1.x)
        try:
            resp = openai.ChatCompletion.create(  # type: ignore[attr-defined]
                model=chosen_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=max_tokens,
                temperature=chosen_temp,
                n=1,
            )
            raw = (resp["choices"][0]["message"]["content"] or "").strip()
            return raw[:requested] if raw else None
        except Exception:
            return None