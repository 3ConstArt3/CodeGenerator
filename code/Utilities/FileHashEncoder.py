import hashlib

from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass(slots=True)
class FileHashEncoder:
    """
    Stream-based hashing utilities.

    :param default_chunk_size: Default chunk size for streaming reads (bytes).
    """
    default_chunk_size: int = 128 * 1024

    def sha256_of_file(self, file_path: str, chunk_size: Optional[int] = None) -> str:
        """
        Compute the SHA-256 hex digest of a file using streaming I/O.

        :param file_path: Path to the file.
        :param chunk_size: Optional override for streaming chunk size in bytes.
        :return: Hex digest string (lowercase).
        :raises FileNotFoundError: If the path does not exist or is not a file.
        :raises ValueError: If chunk size is non-positive.
        :raises OSError: If the file cannot be opened/read.
        """
        path_obj = Path(file_path)
        if not path_obj.exists() or not path_obj.is_file():
            raise FileNotFoundError(f"Path does not exist or is not a file: {file_path}")

        size = int(chunk_size or self.default_chunk_size)
        if size <= 0:
            raise ValueError("chunk_size must be a positive integer")

        hasher = hashlib.sha256()
        try:
            with path_obj.open("rb") as file_stream:
                for block in iter(lambda: file_stream.read(size), b""):
                    hasher.update(block)
        except OSError as exc:
            # Why: keep caller-facing error concise while preserving traceback.
            raise OSError(f"Failed to read file for hashing: {file_path}") from exc
        return hasher.hexdigest()
