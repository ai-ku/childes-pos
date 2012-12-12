#!/usr/bin/env python

import sys
import gzip
flag = False
for l in sys.stdin:
    l = l.strip()
    if l == "-1":  
        flag = True
        continue
    if flag:
        print l
    else:
        print >> sys.stderr,l
