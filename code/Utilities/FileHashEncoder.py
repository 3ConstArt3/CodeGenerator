from pathlib import Path
from hashlib import sha256
from typing import Optional
from dataclasses import dataclass

@dataclass(slots = True)
class FileHashEncoder:

    """
    This class module, provides, the necessary
    stream-based hashing utilities, to correctly
    encode (hash) the passing .txt file's content.

    :param default_chunk_size: The default chunk size for streaming reads.
    """

    default_chunk_size: int = 128 * 1024

    def sha256_of_file(self, file_path: str, chunk_size: Optional[int] = None) -> str:

        """
        Computes the SHA-256 hex digest of the file's content.

        :param file_path: The path to the .txt file.
        :param chunk_size: An optional parameter for streaming the chunk size (bytes).
        :return: The hex digest string of the file's content.
        :raises FileNotFoundError: If the path doesn't exist or is not a valid file.
        :raises ValueError: If the chunk size is a non-positive integer.
        :raises OSError: If the file cannot be opened or read.
        """

        path_object = Path(file_path)
        if not path_object.exists() or not path_object.is_file():
            raise FileNotFoundError(f"The path doesn't exist or is not a valid file: {file_path}")

        size = int(chunk_size or self.default_chunk_size)
        if size <= 0: raise ValueError("The chunk_size, must be a positive integer.")

        hasher = sha256()
        try:

            with path_object.open("rb") as file_stream:
                for block in iter(lambda: file_stream.read(size), b""):
                    hasher.update(block)
        except OSError as exc: raise OSError(f"Failed to read the file at: {file_path}") from exc

        return hasher.hexdigest()
