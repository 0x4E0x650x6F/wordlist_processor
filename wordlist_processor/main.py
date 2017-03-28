#!/usr/bin/env python
# encoding: utf-8


# main.py
# wordlist_processor
#
# Created by 0x4E0x650x6F on 11/02/2017.
# Copyright 2017 0x4E0x650x6F. All rights reserved.

from argparse import ArgumentParser
from os import path
from sys import exit
from distutils.util import strtobool
from optimizer import BaseWordlist


def cmd_interface():
    parser = ArgumentParser()
    clean = parser.add_argument_group('Clean operations',
                                      'Wordlist cleanup')
    encode = parser.add_argument_group('Rencode wordlist',
                                      'Wordlist rencoding')
    parser.add_argument("input",
                        help="Path to the wordlist to clean")
    parser.add_argument("output",
                        help="Path to the cleaned wordlist")
    clean.add_argument("-c", "--clean", action="store_true",
                        help="clean Tabs and spaces")
    clean.add_argument("-t", "--tags", action="store_true",
                        help="clean Tags xml and html")
    clean.add_argument("-d", "--duplicates", action="store_true",
                        help="clean dulicates. Depends on sorting")
    clean.add_argument("-s", "--sort", action="store_true",
                        help="Sorts the wordlist")
    encode.add_argument("-e", "--encoding", type=str,
                        help="Change encoding")

    args = parser.parse_args()
    try:
        if path.isfile(args.input) is False:
            raise ValueError("Invalid file name or Path")
    except ValueError as e:
        print "[*]\t %s" % (e)
        exit(1)
    return args


if __name__ == "__main__":
    print "[*]\tWellcome to wordlist processor\n"

    flin = None
    flout = None
    trim = True
    html = False
    duplicates = True
    sort = True

    args = cmd_interface()
    flin = args.input
    flout = args.output

    sort = args.sort
    trim = args.clean
    html = args.tags
    duplicates = args.duplicates

    if args.encoding and (sort or trim or html or duplicates):
        print "-e and -c| -t | -d| -s are mutually exclusive ..."
        exit(2)

    print "\t[*]\tSource Wordlist:\t %s" % flin
    print "\t[*]\tDestination Wordlist:\t %s" % flout

    print "[*]\tThe folling actions will be executed:\n"
    print "\t[*]\tTrim tabs and spaces: %s" % trim
    print "\t[*]\tRemove Html Tags: %s" % html
    print "\t[*]\tSorts the wordlist: %s" % sort
    print "\t[*]\tRemove Duplicates: %s" % duplicates
    print "[*]\tResults Status:\n"
    cont = raw_input("[-]\tDo you wish to Continue? [y/N]")
    if strtobool(cont):
        print "[*]\tThis might take a while"
        wordlist = BaseWordlist(flin=flin, flout=flout, trim=trim,
                                html=html, sort=sort,
                                duplicates=duplicates)
        wordlist.process()
        wordlist.print_stats()
    else:
        print "[*]\tYou'r choice"
        exit()
