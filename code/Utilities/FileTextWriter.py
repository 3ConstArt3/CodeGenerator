from pathlib import Path
from dataclasses import dataclass

@dataclass(slots = True)
class FileTextWriter:

    """
    Provides all the file utilities that are
    necessary for saving the generated text.

    :param encoding: The text's encoding.
    """
    encoding = "utf-8"

    def write(self, file_path: str, mode, text: str) -> None:

        """
        Writes the generated text to an existing .txt
        file. If the file doesn't exist, it creates it.

        :param file_path: The destination file path.
        :param mode: The mode can be either 'append' (add a line) | 'replace' (overwrite).
        :param text: The text content to write to the file.
        :raises ValueError: If the mode is an invalid literal.
        :raises OSError: If the directories cannot be created or the file cannot be written.
        """

        if mode not in ("append", "replace"):
            raise ValueError("The mode must be either 'append' or 'replace'.")

        target = Path(file_path)
        try: target.parent.mkdir(parents = True, exist_ok = True)
        except OSError as exc: raise OSError(f"Failed to create the parent directories for: {file_path}") from exc

        try:

            mode_letter = "a" if mode == "append" else "w"
            with target.open(mode_letter, encoding = self.encoding, newline = "") as fh:
                fh.write(text + "\n")
        except OSError as exc:
            raise OSError(f"Failed to write to the file: {file_path}") from exc
