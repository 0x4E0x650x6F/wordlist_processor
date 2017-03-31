#!/usr/bin/env python
# encoding: utf-8

#  test_optimizer.py
#  wordlist_processor
#
#  Created by 0x4E0x650x6F on 24/02/2017.
#  Copyright © 2017 0x4E0x650x6F. All rights reserved.

import unittest
from os import remove
from wordlist_processor.optimizer import AbstractWordlist
from wordlist_processor.optimizer import BaseWordlist
from wordlist_processor.optimizer import WordlistEncoder
from wordlist_processor.optimizer import Sort
from os.path import dirname
from os.path import abspath


class TestWordlist(unittest.TestCase):

    def setUp(self):
        self.flin = 'wordlist1.txt'
        self.flout = 'out_wordlist1.txt'
        self.path = '/some/path/'
        self.flerr = ''.join([
            AbstractWordlist.ERROR_SFX,
            self.flin
        ])

    def test_filenames(self):

        wordlist = BaseWordlist(
            flin=''.join([self.path, self.flin]),
            flout=self.flout
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

        wordlist = BaseWordlist(flin=''.join([self.path, self.flin]))

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
        try:
            EXPECTED_SANITIZE_COUNT = 15
            EXPECTED_SANITIZE_HTML_COUNT = 0

            dir_name = dirname(abspath(__file__))

            filename = '%s/data/%s' % (dir_name, 'sort_test_01.lst')
            out_filename = '%s/data/%s' % (dir_name, 'out_sort_test_01.lst')

            wordlist = BaseWordlist(
                flin=filename, flout=out_filename, sort=True)
            wordlist.process()

            self.assertEqual(EXPECTED_SANITIZE_COUNT,
                             wordlist.sanitize.get_count())
            self.assertEqual(EXPECTED_SANITIZE_HTML_COUNT,
                             wordlist.sanitize.get_html_count())
        finally:
            remove(out_filename)

    def test_empty_filenames_fails(self):
        with self.assertRaises(ValueError):
            wordlist = BaseWordlist(flin='', flout='')


class TestWordlistEncoder(unittest.TestCase):

    def test_process_encode_utf8(self):
        try:
            EXPECTED_ENCODE_COUNT = 5
            EXPECTED_UNENCODE_COUNT = 34

            dir_name = dirname(abspath(__file__))
            filename = '%s/data/%s' % (dir_name, 'enc_test_02.lst')
            out_filename = '%s/data/%s' % (dir_name,
                                           'out_enc_test_02.lst')

            wordlist = WordlistEncoder(flin=filename, flout=out_filename,
                                       src_encoding='iso-8859-8',
                                       dst_encoding='utf-8')
            wordlist.process()
            wordlist.print_stats()
            self.assertEqual(EXPECTED_ENCODE_COUNT,
                             wordlist.encoder.get_converted_count())
            self.assertEqual(EXPECTED_UNENCODE_COUNT,
                             wordlist.encoder.get_unconverted_count())
        finally:
            remove(out_filename)
            remove(wordlist.flerr)

    def test_process_encode_latin1(self):
        try:
            EXPECTED_ENCODE_COUNT = 39
            EXPECTED_UNENCODE_COUNT = 0

            dir_name = dirname(abspath(__file__))
            filename = '%s/data/%s' % (dir_name, 'enc_test_01.lst')
            out_filename = '%s/data/%s' % (dir_name,
                                           'out_enc_test_01.lst')

            wordlist = WordlistEncoder(flin=filename, flout=out_filename,
                                       src_encoding='latin_1',
                                       dst_encoding='utf-8')
            wordlist.process()
            wordlist.print_stats()
            self.assertEqual(EXPECTED_ENCODE_COUNT,
                             wordlist.encoder.get_converted_count())
            self.assertEqual(EXPECTED_UNENCODE_COUNT,
                             wordlist.encoder.get_unconverted_count())
        finally:
            remove(out_filename)
            remove(wordlist.flerr)


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
            sort = Sort(duplicates=True)  # enable dupl removal
            for word in sort.sort(input_file):
                words.append(word)

            self.assertEqual(words, self.EXPECTED)
