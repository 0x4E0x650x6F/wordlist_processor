#!/usr/bin/env python
# encoding: utf-8

#  optimizer.py
#  wordlist_processor
#
#  Enconding and decoding functions
#  Created by 0x4E0x650x6F on 24/02/2017.
#  Copyright © 2017 0x4E0x650x6F. All rights reserved.

from os import remove
from os import path
from os.path import dirname
from os.path import basename
from tempfile import gettempdir
from itertools import islice, cycle
import heapq

from .normalizer import Sanitize

class Wordlist(object):

    """
        Base definition of a wordlist takes a 
        wordlist file as parameter extracts the
        path and filename from wich a file for 
        unhandled words from the wordlist is created 
        aka error wordlist
    """

    ERROR_FILENAME_SUFIX = 'err_'
    OUT_FILENAME_SUFIX = 'out_'
    CLEAN_FILENAME_SUFIX = 'clean_'
    
    def __init__(self,  flin, flout=None,
                 trim=True, html=False,
                 sort=True, duplicates=True,
                 rencoding=False):
        """
            :param flin: path the filename
            :type flin: String
            :param flout: path the filename
            :type flout: String
            :param trim: path the filename
            :type trim: Boolean defaults to true
            :param html: path the filename
            :type html: Boolean defaults to true
            :param sort: path the filename
            :type sort: Boolean defaults to true
            :param duplicates: path the filename
            :type duplicates: Boolean defaults to true
            :param rencoding: path the filename
            :type rencoding: Boolean defaults to true
        """
        if flin:
           self.flin_fqdn = flin
           self.flin_path = dirname(flin)
           self.flin = basename(flin)
           self.flerr = ''.join([
                                 self.ERROR_FILENAME_SUFIX,
                                 self.flin
                                ])
        else:
            raise ValueError("Invalid wordlist file or path")

        if flout:
           self.flout_fqdn = flout
           self.flout = basename(flout)
           self.flout_path = flout
        else:
           self.flout = ''.join([
                                 self.OUT_FILENAME_SUFIX,
                                 self.flin
                                ])

           self.flout_path = ''.join([
                                      self.flin_path,
                                      '/',
                                    ])

           self.flout_fqdn = ''.join([
                                      self.flout_path,
                                      self.flout
                                     ])
        self.sort_filename = ''.join([
                                 self.CLEAN_FILENAME_SUFIX,
                                 self.flin
                                 ])
        self.clean_file_fqdn = path.join(
                                    self.flin_path, '%s' % self.sort_filename
                                    )
        self.trim = trim
        self.html = html
        self.sort = sort
        self.duplicates = duplicates
        self.rencoding = rencoding
        # After the paths been set its time to create
        # instanciate the operations
        self.sanitize = Sanitize()
        self.sorting = Sort(duplicates = self.duplicates)

    def get_filename(self):
        """
            :return: flin: Returns the Wordlist filename
            :type flin: String
        """
        return self.flin

    def get_err_filename(self):
        """
            :return: flerr: Returns the Wordlist filename
            :type: flerr: String
        """
        return self.flerr
    
    def get_out_filename(self):
        """
            :return: flout: Return the wordlist filename
            :type: flout: String
        """
        return self.flout
    
    def print_stats(self):
        print "[*]\tNumber of spaces removed %d" % \
            (self.sanitize.get_count())
        print "[*]\tNumber of html tags removed %d" % \
            (self.sanitize.get_html_count())
        
        print "[*]\tNumber of duplicates removed %d" % \
            (self.sorting.get_count())

    def __clean(self, word):
        if self.html:
           return self.sanitize.clean(word)
        else:
           return self.sanitize.trim(word)

    def __pre_prosess(self):
        with open(self.flin_fqdn, 'r') as input_file, \
                open(self.clean_file_fqdn, 'w') as out_file:
            for line in input_file:
                out_file.write(self.__clean(line))
    
    def process(self):
        """
            Implement Wordslist processing implementation
            Clean, sort, remove duplicates.
        """
        self.__pre_prosess()
        if self.sort:
            with open(self.clean_file_fqdn, 'rb', 64*1024) as input_file, \
                    open(self.flout_fqdn, 'wb', 64*1024) as out_file:
                    for word in self.sorting.sort(input_file):
                        out_file.write(word)
        remove(self.clean_file_fqdn)


class Sort(object):

    """
    based on Recipe 466302: Sorting big files the Python 2.4 way
    based on code posted by Scott David Daniels in c.l.p.
    http://groups.google.com/group/comp.lang.python/msg/484f01f1ea3c832d
    """

    def __init__(self, duplicates, buffer_size=32000):
        self.duplicates = duplicates
        self.buffer_size = buffer_size
        self.duplicate_count = 0
        self.sanitize = Sanitize()

    def __merge(self, *iterables):
        last = object()
        for element in heapq.merge(*iterables):
            # make shore sorting doen't get screwd
            # even if trim and html removal should
            # happend before better save than sorry
            # element = self.sanitize.trim(element)
            if self.duplicates == True:
                if element != last:
                    last = element
                    yield element
                else:
                    self.duplicate_count += 1
            else:
                yield element

    def get_count(self):
        return self.duplicate_count

    def sort(self, input_iterator):
        tempdirs = []
        chunks = []
        tempdir = gettempdir()

        print "[*]\tUsing temporary directorys %s" % tempdir

        tempdirs.append(tempdir)
        try:
            input_iterator = iter(input_iterator)
            
            for tempdir in cycle(tempdirs):
                islice_iter = islice(input_iterator, self.buffer_size)
                current_chunk = list(islice_iter)
                if not current_chunk:
                    break
                current_chunk.sort()
                temp_fqdn = path.join(tempdir, '%06i' % len(chunks))
                output_chunk = open(temp_fqdn, 'w+b', 64*1024)
                chunks.append(output_chunk)
                output_chunk.writelines(current_chunk)
                output_chunk.flush()
                output_chunk.seek(0)
        
            print "[*]\tFinished sorting chunks"
            print "[*]\tMerging chunks"

            for word in self.__merge(*chunks):
                yield word
        finally:
            for chunk in chunks:
                try:
                    print "[*]\tClosing temporary file %s" % chunk.name
                    chunk.close()
                    remove(chunk.name)
                except Exception:
                    print '''[*]\t An error ocurred while 
                        closing the chunks'''
