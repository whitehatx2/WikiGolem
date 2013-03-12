#!/usr/bin/env python
#Data cleasing and blacklisting is based on the logic used in
#trendingtopics.org
import sys
import os
import re
import urllib 

#doing date manipulation 
try:
# See if we are running on Hadoop cluster
    filepath = os.environ["map_input_file"] 
    filename = os.path.split(filepath)[-1]
except KeyError:
# sample file for use in testing...
    filename = 'pagecounts-20090419-020000.txt'  
#printing the filename
#print filename
date = filename.split('-')[1]
#print date  

# Excludes pages outside of namespace 0 (ns0)
namespace_titles_regex = re.compile('(Media|Special' + 
'|Talk|User|User_talk|Project|Project_talk|File' +
'|File_talk|MediaWiki|MediaWiki_talk|Template' +
'|Template_talk|Help|Help_talk|Category' +
'|Category_talk|Portal|Wikipedia|Wikipedia_talk)\:(.*)')

# More exclusions
first_letter_is_lower_regex = re.compile('([a-z])(.*)')
image_file_regex = re.compile('(.*).(jpg|gif|png|JPG|GIF|PNG|txt|ico)')

# Exclude Mediawiki boilerplate
blacklist = [
'404_error/',
'Main_Page',
'Hypertext_Transfer_Protocol',
'Favicon.ico',
'Search'
]

def clean_anchors(page):
  # pages like Facebook#Website really are "Facebook",
  # ignore/strip anything starting at # from pagename
  anchor = page.find('#')
  if anchor > -1:
    page = page[0:anchor]
  return page  


def is_valid_title(title):
  is_outside_namespace_zero = namespace_titles_regex.match(title)
  if is_outside_namespace_zero is not None:
    return False
  islowercase = first_letter_is_lower_regex.match(title)
  if islowercase is not None:
    return False
  is_image_file = image_file_regex.match(title)
  if is_image_file:
    return False  
  has_spaces = title.find(' ')
  if has_spaces > -1:
    return False
  if title in blacklist:
    return False   
  return True  
  
  
# input comes from STDIN (standard input)
for line in sys.stdin:
# remove leading and trailing whitespace
    line = line.strip()
# split the line into words
    words = line.split()
# increase counters
#    for word in words:
# write the results to STDOUT (standard output);
# what we output here will be the input for the
# Reduce step, i.e. the input for reducer.py
#
# tab-delimited; the trivial word count is 1
#        print '%s\t%s' % (word, 1)
    if is_valid_title(words[1]):
        title = clean_anchors(urllib.unquote_plus(words[1]))
        if len(title) > 0 and title[0] != '#':
            if(( words[0] == 'en') & (int(words[2]) > 100)):
                print '%s\t%s' % ((date+title),words[2])
