# -*- coding: utf-8 -*-


import unittest
import main as m


class SimpleCase(unittest.TestCase):
    test_string_1: str = "Фёдор Михайлович Достоевский".lower()
    expected_string_transcription_1: str = "Fiodor Michajłowicz Dostojewskij".lower()
    expected_string_transliteration_1: str = "Fëdor Mihajlovič Dostoevskij".lower()

    def testSetUp(self):
        translator: m.Translator = m.Translator(self.test_string_1, m.Mode.BOTH)
        self.assertEqual(self.test_string_1, translator.text_old)
        self.assertEqual(translator.method, m.Mode.BOTH)

    def test_transcript(self):
        translator: m.Translator = m.Translator(self.test_string_1, m.Mode.TRANSCRIPTION)
        translator.start()
        self.assertEqual(self.expected_string_transcription_1, translator.text_new)

    def test_translate(self):
        translator: m.Translator = m.Translator(self.test_string_1, m.Mode.TRANSLITERATION)
        translator.start()
        self.assertEqual(self.expected_string_transliteration_1, translator.text_new)


if __name__ == "__main__":
    unittest.main(verbosity=2)
