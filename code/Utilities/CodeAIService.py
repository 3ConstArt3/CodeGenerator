import os

from typing import Optional
from dataclasses import dataclass, field

from Research.CodeGenerator.Utilities.DataManager import DataManager
from Research.CodeGenerator.Utilities.TextGenerator import TextGenerator
from Research.CodeGenerator.Utilities.FileTextWriter import FileTextWriter
from Research.CodeGenerator.Utilities.FileHashEncoder import FileHashEncoder

os.environ["OPENAI_API_KEY"] = ("your_api_key")

@dataclass(slots = True)
class CodeAIService:

    """
    A high-level code AI service that composes
    hashing, generation and writing utilities.

    :param pipeline: The text generation pipeline.
    :param writer: The file writer utility.
    :param hasher: The file hashing utility.
    """

    pipeline: TextGenerator = field(default_factory = TextGenerator)
    writer: FileTextWriter = field(default_factory = FileTextWriter)
    hasher: FileHashEncoder = field(default_factory = FileHashEncoder)

    def randomize_file(
        self,
        file_path: str,
        mode: Optional[str] = "append",
        char_length: Optional[int] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        data_path: Optional[str] = "Data/data_manager.jsonl",
        encoding: str = "utf-8"
    ) -> str:

        """
        Creates | modifies a file with the AI generated text
        and saves the generated data, into a .jsonl file.

        :param file_path: The target path to create or modify.
        :param mode: 'Append' to add a line or 'replace' to overwrite the file.
        :param char_length: The desired approximate character length.
        :param model: The optional model to override the default.
        :param temperature: The optional temperature to override the default.
        :param data_path: The destination (.jsonl) file path for the data.
        :param encoding: The text's preferred encoding.
        :return: The exact text that was written.
        """

        generated = self.pipeline.generate(
            char_length = char_length,
            model = model,
            temperature = temperature,
        )

        sanitized = (generated or "").strip() or "(empty-generation)"
        self.writer.write(file_path = file_path, mode = mode, text = sanitized)
        file_hash = self.hasher.sha256_of_file(file_path = file_path)

        if data_path:

            manager = DataManager(
                data_path = data_path,
                encoding = encoding,
                ensure_dir = True,
                dedup_by_hex = False,
                time_mode = "local"
            )
            manager.append_text(sanitized, file_hash = file_hash)

        return sanitized

    def encode_file(self, file_path: str, chunk_size: Optional[int] = None) -> str:

        """
        Computes the SHA-256 hex digest of the file's content.

        :param file_path: The path to the .txt file.
        :param chunk_size: An optional parameter for streaming the chunk size.
        :return: The hex digest string of the file's content.
        """

        return self.hasher.sha256_of_file(file_path = file_path, chunk_size = chunk_size)
