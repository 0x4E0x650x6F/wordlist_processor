#!/usr/bin/env python
# encoding: utf-8

#  optimizer.py
#  wordlist_processor
#
#  Enconding and decoding functions
#  Created by 0x4E0x650x6F on 24/02/2017.
#  Copyright © 2017 0x4E0x650x6F. All rights reserved.

import heapq
import codecs
from os import remove
from os import close
from os import path
from abc import ABCMeta
from abc import abstractmethod
from os.path import dirname
from os.path import basename
from tempfile import gettempdir
from itertools import islice, cycle
from normalizer import Sanitizer
from normalizer import Encoder


class AbstractWordlist:
    __metaclass__ = ABCMeta

    ERROR_SFX = 'err_'
    OUT_SFX = 'out_'
    CLEAN_SFX = 'clean_'

    def __init__(self, flin=None, flout=None):
        """
            :param flin: path the filename
            :type flin: String
            :param flout: path the filename
            :type flout: String
        """
        if flin:
            self.flin = flin
            self.flin_path = dirname(flin)
            self.flin_name = basename(flin)
        else:
            raise ValueError("Invalid wordlist file or path")

        if flout:
            self.flout = flout
            self.flout_name = basename(flout)
            self.work_path = dirname(flout)
        else:
            self.flout_name = self.__build_flname(self.OUT_SFX,
                                                  self.flin_name)
            self.work_path = './'
            self.flout = self.__getpath(self.work_path,
                                        self.flout_name, relative=True)

        # Temp filename used to store the words after clean
        self.flclean_name = self.__build_flname(self.CLEAN_SFX,
                                                self.flin_name)
        self.flclean = self.__getpath(self.work_path,
                                      self.flclean_name)

        # Error file name used to store words lead to error
        self.flerr_name = self.__build_flname(self.ERROR_SFX,
                                              self.flin_name)
        self.flerr = self.__getpath(self.work_path,
                                    self.flerr_name)
        self.sanitize = Sanitizer()

    def __build_flname(self, sufix, flname):
        return ''.join([sufix, flname])

    def __getpath(self, path, flname, relative=False):
        if relative:
            return ''.join(['./', flname])
        else:
            return ''.join([path, '/', flname])

    def get_filename(self):
        """
            :return: flin: Returns the Wordlist filename
            :type flin: String
        """
        return self.flin_name

    def get_err_filename(self):
        """
            :return: flerr: Returns the Wordlist filename
            :type: flerr: String
        """
        return self.flerr_name

    def get_out_filename(self):
        """
        :return: flout: Return the wordlist filename
        :type: flout: String
        """
        return self.flout_name

    def clean(self, word):
        if self.html:
            return self.sanitize.clean(word)
        else:
            return self.sanitize.trim(word)

    @abstractmethod
    def print_stats(self):
        pass

    @abstractmethod
    def pre_prosess(self):
        pass

    @abstractmethod
    def process(self):
        pass


class BaseWordlist(AbstractWordlist):

    def __init__(self, trim=True, html=False,
                 sort=True, duplicates=True, **kwds):
        """
            Base definition of a wordlist takes a
            wordlist file as parameter extracts the
            path and filename from wich a file for
            unhandled words from the wordlist is created
            aka error wordlist
        """
        super(BaseWordlist, self).__init__(**kwds)
        self.trim = trim
        self.html = html
        self.sort = sort
        self.duplicates = duplicates
        # After the paths been set its time to create
        # instanciate the operations
        self.sorting = Sort(duplicates=self.duplicates)

    def print_stats(self):
        print "[*]\tNumber of spaces removed %d" % \
            (self.sanitize.get_count())
        print "[*]\tNumber of html tags removed %d" % \
            (self.sanitize.get_html_count())
        print "[*]\tNumber of duplicates removed %d" % \
            (self.sorting.get_count())

    def pre_prosess(self):
        print "[*]\tClean Temp file  %s" % self.flclean

        flin_file = None
        flclean_file = None
        try:
            flin_file = open(self.flin, 'r')
            flclean_file = open(self.flclean, 'w')
            for line in flin_file:
                tmpline = self.clean(line)
                if tmpline:
                    flclean_file.write(tmpline)
        finally:
            print "[*]\tRemoving tmp file %s" % self.flclean
            if flin_file:
                flin_file.close()
            if flclean_file:
                flclean_file.close()

    def process(self):
        input_file = None
        out_file = None
        try:
            self.pre_prosess()
            if self.sort:
                input_file = open(self.flclean, 'rb', 64 * 1024)
                out_file = open(self.flout, 'wb', 64 * 1024)
                for word in self.sorting.sort(input_file):
                    out_file.write(word)
        finally:
            print "[*]\tRemoving tmp file %s" % self.flclean
            if input_file:
                input_file.close()
            if out_file:
                out_file.close()
            remove(self.flclean)


class WordlistEncoder(AbstractWordlist):

    def __init__(self, src_encoding, dst_encoding='utf8', **kwds):
        super(WordlistEncoder, self).__init__(**kwds)
        self.encoder = Encoder(src_encoding, dst_encoding)

    def print_stats(self):
        print "[*]\tNº Chars Enconded %d" % \
            (self.encoder.get_converted_count())
        print "[*]\tNº Chars Not Encoded %s" % \
            (self.encoder.get_unconverted_count())

    def pre_prosess(self):
        pass

    def process(self):
        input_file = None
        out_file = None
        err_file = None
        try:
            input_file = open(self.flin, 'rt')
            out_file = codecs.open(self.flout, 'wt', encoding='utf-8')
            err_file = codecs.open(self.flerr, 'wb')
            for word in input_file:
                try:
                    rencode = self.encoder.convert(word)
                    out_file.write(rencode)
                except UnicodeError as e:
                    print "error %s " % e
                    err_file.write(word)

        except UnicodeError as e:
            print "[*]\tError Reading file with encoding %s" \
                % self.file_encoding
            raise e
        finally:
            print "[*]\Closing tmp file %s" % self.flin
            if input_file:
                input_file.close()
            if err_file:
                err_file.close()
            if out_file:
                out_file.close()


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
        self.sanitize = Sanitizer()

    def __merge(self, *iterables):
        last = object()
        for element in heapq.merge(*iterables):
            # make shore sorting doen't get screwd
            # even if trim and html removal should
            # happend before better save than sorry
            # element = self.sanitize.trim(element)
            if self.duplicates:
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
                output_chunk = open(temp_fqdn, 'w+b', 64 * 1024)
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
