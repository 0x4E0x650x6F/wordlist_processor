#!/usr/bin/env python
# encoding: utf-8

#  test_optimizer.py
#  wordlist_processor
#
#  Created by 0x4E0x650x6F on 24/02/2017.
#  Copyright © 2017 0x4E0x650x6F. All rights reserved.

import unittest
from os import remove
from wordlist_processor.optimizer import Wordlist
from wordlist_processor.optimizer import Sort
from os.path import dirname
from os.path import abspath


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

    def test_process(self):
        EXPECTED_SANITIZE_COUNT = 15
        EXPECTED_SANITIZE_HTML_COUNT = 0
        
        dir_name = dirname(abspath(__file__))
        filename = '%s/%s' % (dir_name, '/data/sort_test_01.lst')
        wordlist = Wordlist(filename, sort=True)
        wordlist.process()
        out_file = wordlist.get_out_filename()
        out_fqdn = '%s/data/%s' % (dir_name, out_file)
        
        self.assertEqual(EXPECTED_SANITIZE_COUNT,
                         wordlist.sanitize.get_count())
        self.assertEqual(EXPECTED_SANITIZE_HTML_COUNT,
                         wordlist.sanitize.get_html_count())
        remove(out_fqdn)
    
    def test_empty_filenames_fails(self):
        with self.assertRaises(ValueError):
             wordlist = Wordlist('','')


class TestSort(unittest.TestCase):

    def setUp(self):
        self.EXPECTED = [
                         "1\n",
                         "1111\n",
                         "1234567\n",
                         "123d\n",
                         "1990\n",
                         "54321\n",
                         "7\n",
                         "angelica\n",
                         "mara\n",
                         "markinho\n",
                         "pepe\n",
                        ]
        self.dir_name = dirname(abspath(__file__))
    
    def test_sorting_and_duplicate_removal(self):
        words = []
        filename = '%s/%s' % (self.dir_name, '/data/sort_test_02.lst')
        with open(filename) as input_file:
            sort = Sort(duplicates=True) # enable dupl removal
            for word in sort.sort(input_file):
                words.append(word)

            self.assertEqual(words, self.EXPECTED)
