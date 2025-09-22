from pathlib import Path
from dataclasses import dataclass

@dataclass(slots=True)
class FileTextWriter:
    """
    File I/O utilities for writing generated text.

    :param encoding: Text encoding for file operations.
    """
    encoding: str = "utf-8"

    def write(self, file_path: str, mode, text: str) -> None:
        """
        Write text to a file, creating parent dirs if needed.

        :param file_path: Destination file path.
        :param mode: 'append' to add a line; 'replace' to overwrite.
        :param text: Text content to write (newline appended).
        :raises ValueError: If mode is invalid.
        :raises OSError: If directories cannot be created or file cannot be written.
        """
        if mode not in ("append", "replace"):
            raise ValueError("mode must be 'append' or 'replace'")

        target = Path(file_path)
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise OSError(f"Failed to create parent directories for: {file_path}") from exc

        try:
            if mode == "append":
                with target.open("a", encoding=self.encoding, newline="") as fh:
                    fh.write(text + "\n")
            else:
                with target.open("w", encoding=self.encoding, newline="") as fh:
                    fh.write(text + "\n")
        except OSError as exc:
            raise OSError(f"Failed to write to file: {file_path}") from exc