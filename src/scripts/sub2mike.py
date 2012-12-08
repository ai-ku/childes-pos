#!/usr/bin/env python

import sys
import gzip
from itertools import izip
from collections import defaultdict as dd

ans = []
sub = []
ansH = dd(int)
subH = dd(int)


for line in open(sys.argv[1]):
    l = line.strip().split()
    if l[0] == "##": continue
    if l[2] not in ansH:
        ansH[l[2]] = len(ansH)
    ans.append(l[2])
    
for l in gzip.open(sys.argv[2]):
    ll = l.strip().split()
    w = ll.pop(0)
    for s in ll:
        if s not in subH:
            subH[s] = len(subH)
    sub.append(ll)

if len(ans) != len(ans):
    sys.exit("Error in shift subs:{0} ans:{1}\n".format(len(sub), len(ans)))

print >>sys.stderr, ">>>", len(ans), len(subH), len(ansH)
clab = ["0"] * len(ansH)
for (s,a) in zip(sub,ans):
    ivec = [0] * len(subH)
    clab[ansH[a]] = "1"
    print "CLAMP Input ALL FULL ",
    for si in s:
        ivec[subH[si]] += 1
    print " ".join(map(str, ivec))
    print "TARGET Output 2 FULL " + " ".join(clab) + "\n;"
    clab[ansH[a]] = "0"
