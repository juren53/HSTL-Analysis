#!/usr/bin/python3

import os
import sys

#file = sys.argv[1]
file = "/home/juren/Projects/HST-Zyimage-Project/ZyFiles/TEXT/LST_thru.txt"

with open(file) as f:
    lines = f.read().splitlines()



os.chdir('/home/juren/Projects/HST-Zyimage-Project/ZyFiles/TEXT')

for l in lines:
    with open(l, 'r') as file:
        your_string = file.read().replace('\n', '')

    your_string = your_string.replace("thru", " thru ")

    list_of_words = your_string.split()
    next_word = list_of_words[list_of_words.index("thru") + 1]
    print(l, next_word)


