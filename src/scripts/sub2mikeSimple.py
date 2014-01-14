#!/usr/bin/env python

import sys
import gzip
from itertools import izip
from collections import defaultdict as dd

data = []
ansH = dd(int)
subH = dd(int)
cons = 0
split = 0

for (ii,line) in enumerate(sys.stdin): ## place of this file is fixed
        l = line.strip().split("\t")
        if l[0] == "-1": 
            data.append(l[0])
            cons -= 1
            split = ii
            continue
        if l[2] not in ansH:
            ansH[l[2]] = len(ansH)
        arr = []
        arr.append(ansH[l[2]])        
        substitutes = l[3].strip().split()
        for s in substitutes:
            if s not in subH:
                subH[s] = len(subH)
            arr.append(subH[s])
        data.append(arr)

print >>sys.stderr, len(data) + cons, len(subH), len(ansH)
clab = ["0"] * len(ansH)

for d in data:
    if d == "-1":
        print "-1"
        continue
    ivec = [0] * len(subH)
    clab[d[0]] = "1"
    print "CLAMP Input ALL FULL ",
    for si in d[1:]:
        ivec[si] += 1
    print " ".join(map(str, ivec))
    print "TARGET Output 2 FULL " + " ".join(clab) + "\n;"
    clab[d[0]] = "0"
