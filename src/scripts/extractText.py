#!/usr/bin/env python

# extracts text from our CHILDES format
# reads from stdin

import sys

for l in sys.stdin:
  larr = l.strip().split()
  for t in larr:
    warr = t.split("/")  
    if warr:
      print warr[0],
  print
