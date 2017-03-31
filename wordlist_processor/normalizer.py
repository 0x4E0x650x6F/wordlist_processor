#!/usr/bin/env python
# encoding: utf-8

#  normalizer.py
#  wordlist_processor
#
#  Created by 0x4E0x650x6F on 25/02/2017.
#  Copyright © 2017 0x4E0x650x6F. All rights reserved.
from bleach import clean


class Encoder(object):

    """
        Converts from one encoding to the other, and
        keeps count of the words converted successfully
        and unsuccessfuly.

    """

    def __init__(self, src_encoding, dst_encoding='utf-8'):
        """
            :param src_encoding: Original encoding
            :param dst_encoding: Destination encoding defaults to
            utf8
            :type src_encoding: String eg: utf-8 uft-16.
            :type dst_encoding: String eg: utf-8 uft-16 defaults
            utf8
        """
        self.src_encoding = src_encoding
        self.dst_encoding = dst_encoding
        self.converted_count = 0
        self.unconverted_count = 0

    def get_converted_count(self):
        return self.converted_count

    def get_unconverted_count(self):
        return self.unconverted_count

    def convert(self, word):
        """
            Convert a String from an encoding to another
            :param word: Word to be converted
            :type word: String eg:
        """
        try:
            # recover the original encoding
            # fix the string
            sword = word.decode(self.src_encoding) \
                .encode(self.src_encoding)
            # convert the string to expected encoding
            uword = sword.decode(self.dst_encoding)
            self.converted_count += 1
            return uword
        except UnicodeError as e:
            self.unconverted_count += 1
            print "[*]\tFaild to convert\t %s" % word
            raise e


class Sanitizer(object):

    """
        Removes spaces or tabs, and html tags
        them calculates number removed char's
        the counts are calculated speratly
    """

    TAB_CHAR = "\t"
    SPACE_CHAR = " "

    def __init__(self):
        # tabs included
        self.spaces_count = 0
        self.html_count = 0

    def get_count(self):
        return self.spaces_count

    def get_html_count(self):
        return self.html_count

    def trim(self, word):
        """
            Removes the spaces tabs and updates the count
            :param word: word or line
            :type word: String
            exmaple:
            '<space>bla<space>bleh<space>' become
            'blableh'
        """
        clean_word = word.replace(self.TAB_CHAR, "") \
            .replace(self.SPACE_CHAR, "")

        self.spaces_count += self.__calc_removed(word, clean_word)
        if (len(clean_word) - clean_word.count('\n')) == 0:
            clean_word = None
        return clean_word

    def clean(self, word):
        """
            Rremoves html tags from string and updates the count
            a this point html encoded chars are kept
            :param word: word or line
            :type word: String

            example:
            in: '<html>blah</html>' out 'blah'
            in: '<html><p>blah</p></html>' out 'blah'
            in: '<html><body><p>blah</p></body></html>' out 'blah'
            in: '<html><body><p>blah </p></body></html>' out 'blah'
            """

        clean_word = clean(word, tags=[],
                           strip=True, strip_comments=True)
        self.html_count += self.__calc_removed(word, clean_word)
        return self.trim(clean_word)

    def __calc_removed(self, dirty_str, clean_str):
        """
            The diference between the two strings used
            to determine the number of chars removed
            and update the corresponding counter..
            :param dirty_str: word or line before clean
            :type dirty_str: String
            :param dirty_str: word or line before clean
            :type clean_str: String
        """
        return len(dirty_str) - len(clean_str)
