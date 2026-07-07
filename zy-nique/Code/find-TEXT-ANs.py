#!/usr/bin/python3
# find-TEXT-ANs.py

import os
import sys
import pprint

file="/home/juren/Projects/HST-Zyimage-Project/Reports/LIST_TEXT-ANs.txt"


with open(file) as f:
   #line =[]

    for line in f: 

        line = line.replace("<accession_number>", " <accession_number> ")
        line = line.replace("</accession_number>", " </accession_number> ")
     
        list_of_words = line.split()
        next_word = list_of_words[list_of_words.index("<accession_number>") + 1]
        print(list_of_words[0],next_word)


