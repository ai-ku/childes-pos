#!/usr/bin/env python

import sys
import gzip
from itertools import izip
from collections import defaultdict as dd

ans = []
sub = []
ansH = dd(int)
subH = dd(int)
instance = 0
partition = []
path = sys.argv[1]
splitpos = 0
for fi in sys.argv[2:]:
    for line in open(fi + ".fre.stat"): ## place of this file is fixed
        l = line.strip().split()
        if l[0] == "##": continue
        if l[0] == '-1':
            splitpos = len(ans)
            continue
        if l[2] not in ansH:
            ansH[l[2]] = len(ansH)
        ans.append(l[2])
    for l in gzip.open(path + fi + ".pairs.gz"): ## this can be changed
        instance += 1
        ll = l.strip().split()
        w = ll.pop(0)
        for s in ll:
            if s not in subH:
                subH[s] = len(subH)
        sub.append(ll)
    partition.append(str(instance))

if len(ans) != len(sub):
    sys.exit("Error in shift subs:{0} ans:{1}\n".format(len(sub), len(ans)))

print >>sys.stderr, ">>>", len(ans), len(subH), len(ansH), " ".join(partition), splitpos
clab = ["0"] * len(ansH)
ii = 0
for (s,a) in zip(sub,ans):
    ii += 1 
    if ii == splitpos:
        print "-1"
        continue
    ivec = [0] * len(subH)
    clab[ansH[a]] = "1"
    print "CLAMP Input ALL FULL ",
    for si in s:
        ivec[subH[si]] += 1
    print " ".join(map(str, ivec))
    print "TARGET Output 2 FULL " + " ".join(clab) + "\n;"
    clab[ansH[a]] = "0"
