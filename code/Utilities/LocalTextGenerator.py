from dataclasses import dataclass
from typing import Final, Optional

@dataclass(slots=True)
class LocalTextGenerator:
    """
    Local pseudo-random text fallback.

    :param default_length: Default target character length.
    """
    default_length: int = 256

    def generate(self, length_chars: Optional[int] = None) -> str:
        """
        Generate pseudo-random text locally as a safe fallback.

        :param length_chars: Approximate target length in characters.
        :return: Locally generated text.
        """
        import secrets

        target = max(16, int(length_chars or self.default_length))
        WORD_POOL: Final[list[str]] = [
            "ember", "silk", "cobalt", "whisper", "lantern", "hollow", "glimmer", "marble",
            "quartz", "ripple", "velvet", "arbor", "lumen", "willow", "bramble", "cinder",
        ]
        approx_token_len = 5  # incl. space
        words_needed = max(1, target // approx_token_len)
        tokens = [secrets.choice(WORD_POOL) for _ in range(words_needed)]
        sentence = " ".join(tokens).strip()
        return sentence[:target]