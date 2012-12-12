#!/usr/bin/env python

import sys
import gzip
from itertools import izip
from collections import defaultdict as dd

data = []
ansH = dd(int)
subH = dd(int)

path = sys.argv[1]
for line in gzip.open(sys.argv[1]): ## place of this file is fixes
        l = line.strip().split()
        if l[0] == "-1": 
            data.append(l[0])
            continue
        if l[0] not in ansH:
            ansH[l[0]] = len(ansH)
        arr = []
        arr.append(ansH[l[0]])
        for s in l[1:]:
            if s not in subH:
                subH[s] = len(subH)
            arr.append(subH[s])
        data.append(arr)

print >>sys.stderr, ">>>", len(data), len(subH), len(ansH)
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
