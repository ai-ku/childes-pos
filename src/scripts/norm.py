#!/usr/bin/env python

import sys
import math

for l in sys.stdin:
  l = l.strip().split()
  words = l[1::2]
  probs = map(lambda x: 10**float(x), l[2::2])
  norm = sum(probs)
  probs = map(lambda x: x / norm, probs)
  for w,p in zip(words, probs):
    print "%s %g" % (w, p),  
  print  
