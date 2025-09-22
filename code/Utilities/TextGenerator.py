from dataclasses import dataclass, field
from typing import Optional

from Research.CodeGenerator.Utilities.RemoteTextGenerator import RemoteTextGenerator
from Research.CodeGenerator.Utilities.LocalTextGenerator import LocalTextGenerator

@dataclass(slots=True)
class TextGenerator:

    """
    Orchestrates text generation: primary OpenAI, then local fallback.

    :param remote: OpenAI-backed generator.
    :param local: Local fallback generator.
    """
    remote: RemoteTextGenerator = field(default_factory=RemoteTextGenerator)
    local: LocalTextGenerator = field(default_factory=LocalTextGenerator)

    def generate(
        self,
        length_chars: Optional[int] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """
        Generate text via remote first, else local.

        :param length_chars: Approximate target length in characters.
        :param model: Optional model override.
        :param temperature: Optional temperature override.
        :return: Generated text (never None).
        """
        text = self.remote.generate(length_chars=length_chars, model=model, temperature=temperature)
        return text if text is not None else self.local.generate(length_chars=length_chars)