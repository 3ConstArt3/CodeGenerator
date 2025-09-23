import os

from typing import Literal, Optional
from dataclasses import dataclass, field

from Research.CodeGenerator.Utilities.TextGenerator import TextGenerator
from Research.CodeGenerator.Utilities.FileTextWriter import FileTextWriter
from Research.CodeGenerator.Utilities.FileHashEncoder import FileHashEncoder

os.environ["OPENAI_API_KEY"] = ("your_API_key")

Mode = Literal["append", "replace"]

@dataclass(slots = True)
class CodeAIService:

    """
    High-level service that composes hashing, generation, and writing utilities.

    :param pipeline: Text generation pipeline (remote + local).
    :param writer: File writer utility.
    :param hasher: File hashing utility.
    """

    pipeline: TextGenerator = field(default_factory=TextGenerator)
    writer: FileTextWriter = field(default_factory=FileTextWriter)
    hasher: FileHashEncoder = field(default_factory=FileHashEncoder)

    def randomize_file(
        self,
        file_path: str,
        mode: Mode = "append",
        length_chars: Optional[int] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """
        Create/modify a file with generated text. Uses OpenAI first, then local fallback.

        :param file_path: Target path to create/modify.
        :param mode: 'append' to add a line; 'replace' to overwrite the file.
        :param length_chars: Desired character length (approximate).
        :param model: Optional model override for this call.
        :param temperature: Optional temperature override for this call.
        :return: The exact text that was written (without trailing newline).
        :raises ValueError: If mode is invalid.
        :raises OSError: If directories cannot be created or file cannot be written.
        """
        generated = self.pipeline.generate(
            char_length=length_chars,
            model=model,
            temperature=temperature,
        )
        sanitized = generated.strip()
        self.writer.write(file_path=file_path, mode=mode, text=sanitized)
        return sanitized

    def encode_file(self, file_path: str, chunk_size: Optional[int] = None) -> str:
        """
        Compute the SHA-256 hex digest of a file.

        :param file_path: Path to the file.
        :param chunk_size: Optional override for streaming chunk size in bytes.
        :return: Hex digest string (lowercase).
        :raises FileNotFoundError: If the path does not exist or is not a file.
        :raises ValueError: If chunk size is non-positive.
        :raises OSError: If the file cannot be opened/read.
        """
        return self.hasher.sha256_of_file(file_path=file_path, chunk_size=chunk_size)

if __name__ == "__main__":

    service = CodeAIService()

    written_text = service.randomize_file("Data/example.txt", mode="replace")
    encoded_text = service.encode_file("Data/example.txt")
    print(encoded_text if encoded_text else None)
