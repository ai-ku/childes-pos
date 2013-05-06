#!/usr/bin/env python


import sys,gzip
from collections import defaultdict as dd

clumap = dd(lambda: dd(int))
clu = dd(int)

for w,c in zip(gzip.open(sys.argv[1]), sys.stdin):
    c, w = c.strip(), w.strip()
    clumap[c][w] += 1
    clu[c] += 1

for c in sorted(clu.keys(), key=lambda x: clu[x], reverse=True):
    sys.stdout.write("%s(%d)\t" %(c,clu[c]))
    for w in sorted(clumap[c].keys(), key= lambda x: clumap[c][x], reverse=True):
        sys.stdout.write("%s(%d) " % (w, clumap[c][w]))
    sys.stdout.write("\n")
