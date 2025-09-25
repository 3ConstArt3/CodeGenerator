from textwrap import shorten
from dataclasses import dataclass
from typing import Optional, Literal
from Research.CodeGenerator.Utilities.CodeAIService import CodeAIService

Mode = Literal["append", "replace"]

@dataclass(slots = True)
class MainPipeline:

    target_file = "Data/generated_text.txt"
    mode: Mode = "replace"
    char_length: Optional[int] = 256
    model: Optional[str] = None
    temperature: Optional[float] = None

    @staticmethod
    def _welcome_banner() -> None:

        print("\n####################################")
        print("# Welcome to my CodeAI Service! :) #")
        print("####################################\n")

    @staticmethod
    def _notes_block() -> None:

        print("######################################################################")
        print("# Notes                                                              #")
        print("# -----                                                              #")
        print("#                                                                    #")
        print("# This tool generates random text (via your configured pipeline)     #")
        print("# which can be either remote (with the use of AI) or local (with     #")
        print("# a custom random text generator. After generating the text, it      #")
        print("# writes it to a target file (either appending it to the previous    #")
        print("# one, or replacing it with the new one. Then it computes the SHA-   #")
        print("# 256 hash of that file for verification, by encoding it to a        #")
        print("# unique 64 byte character string.                                   #")
        print("#                                                                    #")
        print("# Tip: To reproduce a specified and unique hash, keep the file's     #")
        print("# content stable. If you randomize it again, the hash will change.   #")
        print("######################################################################")

    @staticmethod
    def _step(step_title: str) -> None:

        print("\n--------------------------------------------")
        print(f"[Step] {step_title}")
        print("--------------------------------------------\n")

    @staticmethod
    def _exit_banner() -> None:

        print("\n###############################")
        print("# Thanks for using my app ^_^ #")
        print("###############################")

    def run(self):

        self._welcome_banner()
        self._notes_block()
        service = CodeAIService()

        try:

            self._step("Generating text & writing to file")
            written_text = service.randomize_file(
                file_path = self.target_file,
                mode = self.mode,
                char_length = self.char_length,
                model = self.model,
                temperature = self.temperature,
            )

            preview = shorten(written_text, width = 99, placeholder = " ...")
            print(f"- Bytes written in file  : {len(written_text.encode('utf-8'))}")
            print(f"- Generated text preview : {preview}")

            self._step("Encoding the file's generated content")
            encoded_text = service.encode_file(file_path = self.target_file)
            print(f"- Encoded text : {encoded_text}")
            self._exit_banner()

            raise SystemExit(0)

        except KeyboardInterrupt:
            raise SystemExit(130)

if __name__ == "__main__":

    pipeline = MainPipeline()
    raise SystemExit(pipeline.run())
