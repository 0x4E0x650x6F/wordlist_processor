#!/usr/bin/env python
# encoding: utf-8

#  test_optimizer.py
#  wordlist_processor
#
#  Created by 0x4E0x650x6F on 24/02/2017.
#  Copyright © 2017 0x4E0x650x6F. All rights reserved.

import unittest
from wordlist_processor.optimizer import Wordlist

"""
def test_shellexc(self):
        with open(
            'm3g_thi_cth.lst',
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
        self.flin = 'wordlist1.txt'
        self.flout = 'out_wordlist1.txt'
        self.path = '/some/path/'
        self.flerr = ''.join([
                              Wordlist.ERROR_FILENAME_SUFIX,
                              self.flin
                             ])
    
    def test_filenames(self):
        
        wordlist = Wordlist(
                            ''.join([self.path, self.flin]),
                            self.flout
                            )
        
        self.assertEqual(
                         wordlist.get_filename(), self.flin
                         )

        self.assertEqual(
                         wordlist.get_out_filename(),
                         self.flout
                         )
        self.assertEqual(
                         wordlist.get_err_filename(),
                         self.flerr
                         )

    def test_sorting_and_duplicate_remove(self):
        infile = "/Users/0x4E0x650x6F/Downloads/word.lst"
        outfile = "/Users/0x4E0x650x6F/Downloads/out_word.lst"
        wordlist = Wordlist(infile, outfile, duplicates=True)
        wordlist.process()
        wordlist.print_stats()
    
    def test_default_out_filename(self):
    
        wordlist = Wordlist(''.join([self.path, self.flin]))
        
        self.assertEqual(
                         wordlist.get_filename(),
                         self.flin
                         )
        
        self.assertEqual(
                         wordlist.get_out_filename(),
                         self.flout
                         )
        
        self.assertEqual(
                         wordlist.get_err_filename(),
                         self.flerr
                         )
    
    def test_empty_filenames_fails(self):
        with self.assertRaises(ValueError):
             wordlist = Wordlist('','')
