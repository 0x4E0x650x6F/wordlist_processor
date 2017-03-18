#!/usr/bin/env python
# encoding: utf-8


# main.py
# wordlist_processor
#
# Created by 0x4E0x650x6F on 11/02/2017.
# Copyright 2017 0x4E0x650x6F. All rights reserved.

import argparse
from os import path


if __name__ == "__main__":
    print "[*]\tWellcome to wordlist processor\n"

    flin = None
    flout = None
    trim = True
    html = False
    duplicates = True
    sort = True
    
    parser = argparse.ArgumentParser()
    parser.add_argument("input",
                        help="Path to the wordlist to clean")
    parser.add_argument("output",
                        help="Path to the cleaned wordlist")
    parser.add_argument("-c", "--clean", action="store_true",
                        help="clean Tabs and spaces")
    parser.add_argument("-t", "--tags", action="store_true",
                        help="clean Tags xml and html")
    parser.add_argument("-d", "--duplicates", action="store_true",
                        help="clean dulicates. Depends on sorting")
    parser.add_argument("-s", "--sort", action="store_true",
                        help="Sorts the wordlist")

    try:
        args = parser.parse_args()
        if path.isfile(args.input) == False:
            raise ValueError("Invalid file name or Path")

        flin = args.input
        flout = args.output
        
        sort = args.sort
        trim = args.clean
        html = args.tags
        duplicates = args.duplicates
    except ValueError as e:
        print "[*]\t %s" % (e)


    print "\t[*]\tSource Wordlist:\n\t\t %s" % flin
    print "\t[*]\tDestination Wordlist:\n\t\t %s" % flout

    print "[*]\tThe folling actions will be executed:\n"
    print "\t[*]\tTrim tabs and spaces: %s" % trim
    print "\t[*]\tRemove Html Tags: %s" % html
    print "\t[*]\tSorts the wordlist: %s" % sort
    print "\t[*]\tRemove Duplicates: %s" % duplicates
