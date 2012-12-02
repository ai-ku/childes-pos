#!/usr/bin/env python

import sys
import re
import pprint

tdic = {}
coarse = sys.argv[1]
for l in sys.stdin:
    if not l.strip():
        print 
        continue
    if coarse == "c":
        m = re.search(ur'(.*?)\t(.*?)[\|:].*?$',l)
    else:
        m = re.search(ur'(.*?)\t(.*?)\|.*?$',l)
    if m == None:
        tdic[tag] = 1;
        print l
        continue    
    word, tag = m.group(1), m.group(2)
    tag = re.sub(ur'(\w+#|0)(\S+)',r'\2',tag)
    tdic[tag] = 1;
    print "{0}\t{1}".format(word, tag)
    
print >> sys.stderr, "number of tags", len(tdic.keys()),tdic.keys()

