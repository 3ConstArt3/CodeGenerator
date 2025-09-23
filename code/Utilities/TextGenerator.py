from typing import Optional
from dataclasses import dataclass, field

from Research.CodeGenerator.Utilities.RemoteTextGenerator import RemoteTextGenerator
from Research.CodeGenerator.Utilities.LocalTextGenerator import LocalTextGenerator

@dataclass(slots = True)
class TextGenerator:

    """
    Orchestrates the text generation process
    where the primary generation uses the OpenAI's
    API and then a local generator as a fallback
    if the primary one fails.

    :param remote: The OpenAI-backed generator.
    :param local: The local fallback generator.
    """

    remote: RemoteTextGenerator = field(default_factory = RemoteTextGenerator)
    local: LocalTextGenerator = field(default_factory = LocalTextGenerator)

    def generate(
        self,
        char_length: Optional[int] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> str:

        """
        Generates random creative text via
        a remote AI generator. If the primary
        generator fails, then it uses a local
        one as a fallback.

        :param char_length: The approximate target length in characters.
        :param model: The optional gpt model to override the default.
        :param temperature: The optional temperature to override the default.
        :return: The processed generated text.
        """

        text = self.remote.generate(
            char_length = char_length,
            model = model,
            temperature = temperature
        )

        return text if text is not None else self.local.generate(char_length = char_length)
