#!/usr/bin/env python
# encoding: utf-8

#  test_wrdlstcleaner.py
#  wordlist_processor
#
#  Created by 0x4E0x650x6F on 25/02/2017.
#  Copyright © 2017 0x4E0x650x6F. All rights reserved.

import unittest
from wordlist_processor.normalizer import Sanitizer
from wordlist_processor.normalizer import Encoder
import codecs
from os.path import dirname
from os.path import abspath


class TestEncoding(unittest.TestCase):

    def test_convert_from_utf16_to_utf8_faild(self):

        with self.assertRaises(UnicodeDecodeError):
            encoder = Encoder('utf_16', 'utf8')
            result = encoder.convert("√º√§√∂12345")


class TestNormalizer(unittest.TestCase):

    def test_str_clean(self):
        INPUT = " adsadasd adsasd "
        EXPECTED = "adsadasdadsasd"
        NUMBER_OF_SPACES = 3

        normalizer = Sanitizer()
        strclean = normalizer.trim(INPUT)
        self.assertEqual(NUMBER_OF_SPACES, normalizer.get_count())
        self.assertEqual(EXPECTED, strclean)

    def test_str_empty(self):
        INPUT = "\n"
        EXPECTED = None
        NUMBER_OF_SPACES = 0

        normalizer = Sanitizer()
        strclean = normalizer.trim(INPUT)

        self.assertEqual(EXPECTED, strclean)

    def test_single_level_html(self):

        HTML_IN = "<html> blah</html>"
        HTML_TAGS = "<html></html>"
        EXPECTED = "blah"
        NUMBER_OF_SPACES = 1

        normalizer = Sanitizer()
        strclean = normalizer.clean(HTML_IN)
        self.assertEqual(EXPECTED, strclean)
        self.assertEqual(NUMBER_OF_SPACES, normalizer.get_count())
        self.assertEqual(len(HTML_TAGS), normalizer.get_html_count())

    def test_rand_html_tags(self):

        HTML_IN = "ass<html> blah</html>"
        HTML_TAGS = "<html></html>"
        EXPECTED = "assblah"
        NUMBER_OF_SPACES = 1

        normalizer = Sanitizer()
        strclean = normalizer.clean(HTML_IN)
        self.assertEqual(EXPECTED, strclean)
        self.assertEqual(NUMBER_OF_SPACES, normalizer.get_count())
        self.assertEqual(len(HTML_TAGS), normalizer.get_html_count())

    def test_rand_invalid_html_tags(self):

        HTML_IN = "ass<a> blah</>"
        HTML_TAGS = "<a></>"
        EXPECTED = "assblah"
        NUMBER_OF_SPACES = 1

        normalizer = Sanitizer()
        strclean = normalizer.clean(HTML_IN)
        self.assertEqual(EXPECTED, strclean)
        self.assertEqual(NUMBER_OF_SPACES, normalizer.get_count())
        self.assertEqual(len(HTML_TAGS), normalizer.get_html_count())

    def test_rand_invalid_html_tags2(self):

        HTML_IN = "ass<a> blah</a>"
        HTML_TAGS = "<a></a>"
        EXPECTED = "assblah"
        NUMBER_OF_SPACES = 1

        normalizer = Sanitizer()
        strclean = normalizer.clean(HTML_IN)
        self.assertEqual(EXPECTED, strclean)
        self.assertEqual(NUMBER_OF_SPACES, normalizer.get_count())
        self.assertEqual(len(HTML_TAGS), normalizer.get_html_count())

    def test_rand_invalid_html_tags3(self):

        HTML_IN = "ass<a> blah</>"
        HTML_TAGS = "<a></>"
        EXPECTED = "assblah"
        NUMBER_OF_SPACES = 1

        normalizer = Sanitizer()
        strclean = normalizer.clean(HTML_IN)
        self.assertEqual(EXPECTED, strclean)
        self.assertEqual(NUMBER_OF_SPACES, normalizer.get_count())
        self.assertEqual(len(HTML_TAGS), normalizer.get_html_count())


if __name__ == '__main__':
    unittest.main()
