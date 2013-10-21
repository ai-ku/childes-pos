#!/usr/bin/env python

import sys
from collections import defaultdict as dd
# Takes the average of each tags in the files

fileCounter = 0;
allAcc = dd(int)

for f in sys.stdin:
  fname = f.strip()
  foldAcc = dd(int)
  foldCount = dd(int)
  ans = 0
  for l in open(fname):
    larr = l.strip().split() 
    ans += 1
    foldCount[larr[0]] += 1.
    if larr[0] == larr[1]:
      foldAcc[larr[0]] += 1.
  fileCounter += 1
  for k,v in foldCount.items():
     if k in foldAcc:
       # print k, foldAcc[k] / v
       allAcc[k] += foldAcc[k] / v
      # else:
       # print k, 0

print "# Summary", fileCounter
for k,v in allAcc.items():
  print k, v *1.0 / fileCounter
