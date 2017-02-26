#!/usr/bin/env python
# encoding: utf-8

#  test_main.py
#  wordlist_processor
#
#  Created by 0x4E0x650x6F on 11/02/2017.
#  Copyright © 2017 0x4E0x650x6F. All rights reserved.

import unittest
from wordlist_processor.main import Wordlist


"""
def test_shellexc(self):
        with open(
            '/Users/0x4E0x650x6F/Documents/cracking/dict/m3g_thi_cth.lst',
            'r') as wordlist:
            
            for word in wordlist:
                try:
                    print word.decode('utf_8_sig').encode('utf-8')
                except Exception as e:
                   print "faild"
                    #print word
                    #print word.decode('latin-1').encode('utf-8')
"""


class TestWordlist(unittest.TestCase):

    def setUp(self):
        self.filename = 'wordlist1.txt'
        self.path = '/some/path/'
        self.err_filename = ''.join([
                                     Wordlist.ERROR_FILENAME_SUFIX,
                                     self.filename
                                    ])
    
    def test_filenames(self):
        
        wordlist = Wordlist(''.join([self.path, self.filename]))
        
        self.assertEqual(wordlist.get_filename(), self.filename)
        self.assertEqual(wordlist.get_err_filename(),
                         self.err_filename)
        self.assertEqual(wordlist.get_path(),
                         self.path[:len(self.path) - 1])

    def test_filename_fails(self):
        with self.assertRaises(ValueError):
             wordlist = Wordlist('')


if __name__ == '__main__':
    unittest.main()
