#!/usr/bin/env python
# encoding: utf-8


# wrdlstcleaner.py
# wordlist_processor
#
# Created by 0x4E0x650x6F on 11/02/2017.
# Copyright 2017 0x4E0x650x6F. All rights reserved.

from os.path import dirname
from os.path import basename


class Wordlist(object):

    """
        Base definition of a wordlist takes a 
        wordlist file as parameter extracts the
        path and filename from wich a file for 
        unhandled words from the wordlist
    """

    ERROR_FILENAME_SUFIX = 'err_'
    
    def __init__(self,  wordlist):
        """
            :param wordlist: path the filename
            :type wordlist: String eg:
        """
        if wordlist:
           self.path = dirname(wordlist)
           self.filename = basename(wordlist)
           self.err_filename = ''.join([
                                        self.ERROR_FILENAME_SUFIX,
                                        self.filename])
        else:
            raise ValueError("Invalid wordlist")

    def get_filename(self):
        """
            :return: filename: Returns the Wordlist filename
            :type filename: String
        """
        return self.filename

    def get_err_filename(self):
        """
            :return: err_filename: Returns the Wordlist filename
            :type filename: String
        """
        return self.err_filename

    def get_path(self):
        return self.path



if __name__ == "__main__":
    print "[*] wellcome to wordlist processor"
