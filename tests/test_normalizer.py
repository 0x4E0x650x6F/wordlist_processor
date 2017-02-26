#!/usr/bin/env python
# encoding: utf-8

#  test_wrdlstcleaner.py
#  wordlist_processor
#
#  Created by 0x4E0x650x6F on 25/02/2017.
#  Copyright © 2017 0x4E0x650x6F. All rights reserved.

import unittest
from wordlist_processor.normalizer import Html
from wordlist_processor.normalizer import Sanitize
from wordlist_processor.normalizer import Encoder


class TestEncoding(unittest.TestCase):
    
    def setUp(self):
        self.WORDS = [
                      r"√º√§√∂12345",
                      r"∆*ÅôY'èQ∏~≤wk©á",
                      r"∆.VOòíO(gø$ÎÔs—´Eå¯QÜ",
                      r"∆.œg›≥nÁ∞∂;Î–=g©y"
                    ]
        self.EXPECTED = [
                         r"√º√§√∂12345",
                         r"∆*ÅôY'èQ∏~≤wk©á",
                         r"∆.VOòíO(gø$ÎÔs—´Eå¯QÜ",
                         r"∆.œg›≥nÁ∞∂;Î–=g©y"
                        ]
    
    def test_convert_from_utf16_to_utf8(self):
        encoder = Encoder('utf_8_sig', 'utf8')

        for i in range(len(self.WORDS)):
            self.assertEqual(encoder.convert(self.WORDS[i]), self.EXPECTED[i])
    
    def test_convert_from_utf16_to_utf8_faild(self):
        with self.assertRaises(UnicodeDecodeError):
            encoder = Encoder('utf_16', 'utf8')
            self.assertEqual(encoder.convert(self.WORDS[0]),
                             self.EXPECTED[0])


class TestNormalizer(unittest.TestCase):

    def test_str_clean(self):
        INPUT = " adsadasd adsasd "
        EXPECTED = "adsadasdadsasd"
        NUMBER_OF_SPACES  = 3
        
        normalizer = Sanitize()
        strclean = normalizer.clean(INPUT)
        
        self.assertEqual(NUMBER_OF_SPACES, normalizer.get_count())
        self.assertEqual(EXPECTED, strclean)
    
    def test_single_level_html(self):
        
        HTML_IN = "<html> blah</html>"
        HTML_TAGS = "<html></html>"
        EXPECTED = "blah"
        NUMBER_OF_SPACES  = 1
        
        normalizer = Html()
        strclean = normalizer.clean(HTML_IN)
        self.assertEqual(EXPECTED, strclean)
        self.assertEqual(NUMBER_OF_SPACES, normalizer.get_count())
        self.assertEqual(len(HTML_TAGS), normalizer.get_html_count())
