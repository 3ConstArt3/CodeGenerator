import os
import json

from hashlib import sha256
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Literal, Optional, TypedDict, Iterator, Any

class DataRecord(TypedDict):

    """
    The final shape of a single .jsonl record
    line, that is used by the DataManager in
    to safely save the generated data.
    """

    id: str
    hash: Optional[str]
    text: str
    length: int
    encoding: str
    timestamp: str

@dataclass(slots = True)
class DataManager:

    """
    A minimalistic .jsonl data manager, that saves
    the generated data, in records of the following form:
    ("id", "hash", "text", "length", "encoding", "timestamp")

    Where:
    - "id": Is the SHA-256 computed over the exact text bytes.
    - "hash": Is the resulted hash encoding of the file's content.
    - "timestamp": Is the local (or "utc") timestamp.

    :param data_path: The destination (.jsonl) file path for the data.
    :param encoding: The text's preferred encoding.
    :param ensure_dir: Creates parent directories if True.
    :param dedup_by_hex: Skips appending (when True) if a record with the same "hash" already exists.
    :param time_mode: The "local" (or "utc") mode for the timestamp.
    """

    data_path: str
    encoding: str = "utf-8"
    ensure_dir: bool = True
    dedup_by_hex: bool = False
    time_mode: Literal["local", "utc"] = "local"

    def append_text(self, text: str, file_hash: Optional[str] = None) -> DataRecord:

        """
        Appends a new text record to the .jsonl data manager.
        If `dedup_by_hex` is True and `file_hash` matches a
        previously written record's hash, the record is not
        written again, to avoid possible duplicates.

        :param text: The exact text content to record.
        :param file_hash: The resulted encoding of the file's content.
        :return: The last written record.
        :raises OSError: On directory creation failure or file I/O errors.
        :raises UnicodeError: If writing to the file fails due to the encoding.
        """

        record = self.create_record(text = text, file_hash = file_hash)

        if self.ensure_dir:

            parent_dir = os.path.dirname(self.data_path) or "."
            try: os.makedirs(parent_dir, exist_ok = True)
            except OSError as exc: raise OSError(f"Failed to create parent directory: {parent_dir}") from exc

        if self.dedup_by_hex and self._hex_exists(record["hash"]):
            return record

        try:

            with open(self.data_path, "a", encoding = self.encoding, newline = "") as file_handle:

                file_handle.write(json.dumps(record, ensure_ascii = False))
                file_handle.write("\n")
        except UnicodeError: raise
        except OSError as exc: raise OSError(f"Failed to append to .jsonl file: {self.data_path}") from exc

        return record

    def create_record(self, *, text: str, file_hash: Optional[str] = None) -> DataRecord:

        """
        Builds a minimal data record with the
        necessary information for the generated output.

        :param text: The exact text to encode and hash.
        :param file_hash: The resulted encoding of the file's content.
        :return: The final minimalistic record of data.
        :raises ValueError: If the text cannot be encoded with the provided encoding.
        """

        try: text_bytes = text.encode(self.encoding)
        except LookupError as exc: raise ValueError(f"Unknown encoding: {self.encoding}") from exc
        except UnicodeEncodeError as exc: raise ValueError(f"Text cannot be encoded in {self.encoding}.") from exc

        return {
            "id": sha256(text_bytes).hexdigest(),
            "hash": file_hash,
            "text": text,
            "length": len(text),
            "encoding": self.encoding,
            "timestamp": self._timestamp(),
        }

    def _timestamp(self) -> str:

        """
        Computes an ISO-8601 unique timestamp.

        :return: The timestamp string ("utc" or "local").
        """

        if self.time_mode == "utc":

            return (
                datetime.now(timezone.utc)
                .replace(microsecond = 0)
                .isoformat()
                .replace("+00:00", "Z")
            )

        return datetime.now().astimezone().replace(microsecond = 0).isoformat()

    def _hex_exists(self, hex_digest: str) -> bool:

        """
        Scans the .jsonl file to see if a record with
        the given external hex digest exists, to avoid
        possible duplicates and to prevent errors.

        :param hex_digest: The hex digest to look up for.
        :return: True if a matching record is found.
        :raises OSError: If the file cannot be opened.
        """

        if not hex_digest: return False
        if not os.path.exists(self.data_path): return False

        try:

            for dict_object in self._iter_jsonl_objects():

                digest = dict_object.get("hash") or dict_object.get("hex")
                if digest == hex_digest: return True
        except OSError: raise
        except Exception: return False

        return False

    def _iter_jsonl_objects(self) -> Iterator[dict[str, Any]]:

        """
        Iterates over parsed .jsonl objects from the .jsonl
        file, skipping blank and invalid lines to avoid errors.

        :return: The iterator of dictionary (.json) objects.
        :raises OSError: If the file cannot be opened.
        """

        with open(self.data_path, "r", encoding = self.encoding) as file_handle:

            for raw_line in file_handle:

                line = raw_line.strip()
                if not line: continue

                try: yield json.loads(line)
                except Exception: continue
