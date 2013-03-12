#!/usr/bin/env python

from operator import itemgetter
import sys
import os

current_word = None
current_count = 0
word = None

# input comes from STDIN
for line in sys.stdin:
# remove leading and trailing whitespace
    line = line.strip()

# parse the input we got from mapper.py
    try:
        words = line.split('\t')
    except ValueError:
        print 'ERROR'+line
        continue
# convert count (currently a string) to int
    try:
        count = int(words[1])
        word = words[0]
    except ValueError:
# count was not a number, so silently
# ignore/discard this line
        continue
        
# this IF-switch only works because Hadoop sorts map output
# by key (here: word) before it is passed to the reducer
    if current_word == word:
        current_count += count
    else:
        if current_word:
# write result to STDOUT
            date = current_word[0:8]
            topic = current_word[8:]
            print '%s\t%s-%s-%s\t%s' % ( topic, date[0:4],date[4:6],date[6:8], current_count)
        current_count = count
        current_word = word

# do not forget to output the last word if needed!
if current_word == word:
    print '%s\t%s-%s-%s\t%s' % (current_word[8:], current_word[0:4],current_word[4:6],current_word[6:8] , current_count)
