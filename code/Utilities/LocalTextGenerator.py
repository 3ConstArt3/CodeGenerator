from secrets import SystemRandom
from dataclasses import dataclass, field
from typing import ClassVar, Optional, Sequence

@dataclass(slots = True)
class LocalTextGenerator:

    """
    A local pseudo-random text generator
    that is used as a fallback, in case
    the AI generator fails to generate
    any text content.

    :param default_length: The default target character length.
    """
    default_length = 256

    generator: SystemRandom = field(default_factory = SystemRandom, init = False, repr = False)

    BASE_WORDS: ClassVar[Sequence[str]] = (
        "ember silk cobalt whisper lantern hollow glimmer marble quartz ripple velvet arbor "
        "lumen willow bramble cinder hush drift argent briar aurora moss linen satin obsidian "
        "gale thicket hush hush hush thrum lanterns riverstone amber dusk hollowed echo "
        "willowisp frost serif monolith dune mica loam hustling silver ash grove thistle "
        "harbor zephyr lanternlight moonlit umber linenwork cobblestone vellum inkwell "
        "wicker saffron ochre opal ambergris violet indigo coral basil thyme clover yarrow"
    ).split()

    PSEUDO_SYLLABLES: ClassVar[Sequence[str]] = (
        "lo ra mi sa qua el in or um an su vel mar bri sil lum ven tor cal dra nai vor "
        "sha len thal mir iss kar ul en da phi zor qui ner sal vor li on ix ash ora"
    ).split()

    SUFFIXES: ClassVar[Sequence[str]] = ("ish", "ly", "ful", "less", "ness", "ward", "wise")
    PREFIXES: ClassVar[Sequence[str]] = ("pre", "un", "re", "over", "under", "mis", "anti")
    MID_PUNCTUATION: ClassVar[Sequence[str]] = (",", ",", "-", ":", "...")
    END_PUNCTUATION: ClassVar[Sequence[str]] = (".", ".", ".", ".", "!", "?")

    def generate(self, char_length: Optional[int] = None) -> str:

        """
        Generates pseudo-random text locally as a
        safe fallback, with higher unpredictability.

        :param char_length: The approximate target length in characters.
        :return: The locally generated text.
        """

        target = max(16, int(char_length or self.default_length))
        output: list[str] = []
        while self._total_len_with_spaces(output) < target + 32:
            output.append(self._make_sentence())

        text = " ".join(output)
        return text[:target]

    @staticmethod
    def _total_len_with_spaces(sentences: Sequence[str]) -> int:

        """
        :param sentences: The sequence of sentences.
        :return: The total length plus the single spaces between sentences.
        """

        if not sentences: return 0
        return sum(len(s) for s in sentences) + (len(sentences) - 1)

    def _random_choice(self, sequence: Sequence[str]) -> str:

        """
        :param sequence: A sequence of strings.
        :return: A random element from the sequence.
        """

        return sequence[self.generator.randrange(len(sequence))]

    def _maybe(self, probability: float) -> bool:

        """
        :param probability: The probability (e) [0, 1].
        :return: True if the probabilistic inequality holds.
        """

        return self.generator.random() < probability

    def _double_random_letter(self, word: str) -> str:

        """
        Duplicate a random interior character for mild mutation.

        :param word: The input token.
        :return: The mutated (or the original if too short) token.
        """

        if len(word) < 3: return word
        i = self.generator.randrange(1, len(word) - 1)
        return word[:i] + word[i] + word[i:]

    def _mutate_base(self, word: str) -> str:

        """
        Applies probabilistic mutations to the provided base word.

        :param word: The given base word.
        :return: The mutated version of the base word.
        """

        if self._maybe(0.25): return self._double_random_letter(word)
        if self._maybe(0.30): return f"{word}-{self._random_choice(self.BASE_WORDS)}"
        if self._maybe(0.35): return word + self._random_choice(self.SUFFIXES)
        if self._maybe(0.20): return self._random_choice(self.PREFIXES) + word
        if self._maybe(0.20): return word.title() if self._maybe(0.5) else word.upper()

    def _pseudoword(self) -> str:

        """
        Builds a pseudoword from syllables
        with some small 'random' mutations.

        :return: The generated pseudoword.
        """

        n = self.generator.randint(2, 4)
        parts = [self._random_choice(self.PSEUDO_SYLLABLES) for _ in range(n)]

        word = "".join(parts)
        if self._maybe(0.25): return self._double_random_letter(word)
        if self._maybe(0.20): return word + self._random_choice(self.SUFFIXES)
        if self._maybe(0.15): return word.title()

    def _punctuate(self, tokens: list[str]) -> list[str]:

        """
        Adds light-touch mid-sentence punctuation.

        :param tokens: A list of token words.
        :return: The possibly punctuated tokens.
        """

        if not tokens: return tokens
        for i in range(1, len(tokens) - 1):
            if self._maybe(0.18):
                tokens[i] += self._random_choice(self.MID_PUNCTUATION)

        return tokens

    def _make_sentence(self) -> str:

        """
        Composes a sentence using base words,
        mutations and pseudo-words to enhance
        its unpredictability and randomness.

        :return: A randomized sentence ending with '.', '!' or '?'.
        """

        n_words = self.generator.randint(5, 16)
        words: list[str] = []
        for _ in range(n_words):

            rand_choice = self.generator.random()
            if rand_choice < 0.60: word = self._random_choice(self.BASE_WORDS)
            elif rand_choice < 0.85: word = self._mutate_base(self._random_choice(self.BASE_WORDS))
            else: word = self._pseudoword()
            words.append(word)

        words = self._punctuate(words)
        if words: words[0] = words[0].capitalize()
        end = self._random_choice(self.END_PUNCTUATION)

        return " ".join(words).rstrip(",-:... ") + end
