#!/usr/bin/env python

import sys
import math

ran = -1
if len(sys.argv) == 2:
  ran = 2 * int(sys.argv[1]) + 2 
else:
  ran = -1

for l in sys.stdin:
  l = l.strip().split()
  if ran == -1:
    words = l[1::2]
    probs = map(lambda x: 10**float(x), l[2::2])
  else:
    words = l[1:ran:2]
    probs = map(lambda x: 10**float(x), l[2:ran:2])
  norm = sum(probs)
  probs = map(lambda x: x / norm, probs)
  for w,p in zip(words, probs):
    print "%s %g" % (w, p),  
  print  
