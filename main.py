# -*- coding: utf-8 -*-


from enum import Enum
from typing import List
from rules import TRANSLITERATIONS, TRANSCRIPTIONS, VOWELS


class Mode(Enum):
    TRANSCRIPTION: int = 1
    TRANSLITERATION: int = 2
    BOTH: int = 3

    def __int__(self):
        return self.value


class Translator:
    """
       Translator may work in two modes: transcription and transliteration.
       Index is necessary to keep track of parsed letters to allow check previous
       and next characters.
    """

    def __init__(self, text_old: str, method: Mode = Mode.TRANSCRIPTION):
        self.method = method
        self.text_old = text_old
        self.text_new = ""
        self.index = 0

    def start(self):
        print()
        if self.method == Mode.TRANSLITERATION:
            self.transliterate()
        elif self.method == Mode.TRANSCRIPTION:
            self.transcript()
        else:
            self.transcript()
            self.transliterate()

    def check_next_char(self) -> str:
        """ Checks what is the next letter of old (russian) text. """
        try:
            return self.text_old[self.index + 1]
        except IndexError:
            return ""

    def check_previous_char(self) -> str:
        """ Checks what is the previous letter of old (russian) text. """
        try:
            return self.text_old[self.index - 1]
        except IndexError:
            return ""
        except KeyError:
            return " "

    def transliterate_letter(self, char: str) -> str:
        self.index += 1
        try:
            return TRANSLITERATIONS[char]
        except KeyError:
            # If current character is not a cyrillic letter,
            # just return the original.
            return char

    def transliterate(self):
        new_text: List[str] = []
        for letter in self.text_old.lower():
            new_text.append(self.transliterate_letter(letter))
        self.text_new = "".join(new_text)
        print(self.text_new + "\n")

    def transcript_letter(self, char: str) -> str:
        try:
            letter = TRANSCRIPTIONS[char]
        except KeyError:
            # If current character is not a cyrillic letter,
            # just return the original.
            return char
        else:
            if "_" not in letter:
                # "_" is used as separator for letters that can transcript
                # to several different options.
                return letter
            else:
                s = letter.split("_")
                prev = self.check_previous_char()
                next_ = self.check_next_char()
                if char == "е" or char == "ё":
                    if prev == "" or prev in VOWELS or prev in ("ъ", "ь"):
                        return s[0]
                    elif prev in ("ж", "л", "ц", "ч", "ш", "щ"):
                        return s[1]
                    else:
                        return s[2]
                elif char == "и":
                    if prev == "ь":
                        return s[1]
                    elif prev in ("ж", "ц", "ш"):
                        return s[2]
                    else:
                        return s[0]
                elif char == "л":
                    if next_ in ("е", "ё", "и", "ь", "ю", "я"):
                        return s[0]
                    else:
                        return s[1]
                elif char == "ь":
                    if prev not in VOWELS or prev not in ("л", "ж", "ч", "ш", "щ"):
                        return s[0]
                elif char == "ю" or char == "я":
                    if prev == "" or prev in VOWELS or prev in ("ъ", "ь"):
                        return s[0]
                    elif prev == "л":
                        return s[1]
                    else:
                        return s[2]
        finally:
            # Index has to be incremented at the very end of function;
            # otherwise it would mess checking surrounding letters when
            # parsing cyrillic chars that transcripts to multiple characters.
            self.index += 1

    def transcript(self):
        new_text: List[str] = []
        for letter in self.text_old.lower():
            new_text.append(self.transcript_letter(letter))
        self.text_new = "".join(new_text)
        print(self.text_new + "\n")


if __name__ == "__main__":
    chosen: str = input(
        "Choose script mode:\n1 - transcription, 2 - transliteration, 3 - both"
        "\ndefault: 1 - transcription\n"
    )
    current_mode: Mode
    try:
        current_mode = Mode(int(chosen[0]))
    except (IndexError, ValueError):
        current_mode = Mode.TRANSCRIPTION
    translator: Translator
    while True:
        txt: str = input("\nType text to translate:\n")
        translator = Translator(txt, current_mode)
        translator.start()
        cont: str = input("\nContinue? (any / n)\n")
        if cont != "" and cont[0].lower() == "n":
            break
