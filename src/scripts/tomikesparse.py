#!/usr/bin/env python

import sys,gzip
from collections import defaultdict as dd
from pprint import pprint as pp

frame = dd(int)
framer = dd(int)
tag = dd()
arr = []
tagtype = "fre"

if sys.argv[1] == "pr" or sys.argv[1] == "prbi" or sys.argv[1] == "apr":
    tagtype = "pr"
elif sys.argv[1] == "ps" or sys.argv[1] == "psbi" or sys.argv[1] == "aps":
    tagtype = "ps"  
elif sys.argv[1] == "fle":
    tagtype = "fle"
elif sys.argv[1] == "fre":
    tagtype = "fre"
else:
    sys.exit("Unmatched Tag" + sys.argv[1])
instance = 0

for line in sys.stdin:
    l = line.strip().split("\t")
    if l[0] == "-1":
        arr.append(-1);
        continue
    elif l[1] == "X":
        continue
    instance += 1
    f1,f2 = l[4].split(":")
    if l[3] not in tag:
        tag[l[3]] = len(tag)
    if tagtype == "pr"  and f1 not in frame:
        frame[f1] = len(frame)
        arr.append([frame[f1],tag[l[3]]])
    elif tagtype == "pr":
        arr.append([frame[f1],tag[l[3]]])
    if tagtype == "ps" and f2 not in frame:
        frame[f2] = len(frame)
        arr.append([frame[f2],tag[l[3]]])
    elif tagtype == "ps":
        arr.append([frame[f2],tag[l[3]]])
    if tagtype == "fre" and l[4] not in frame:
        frame[l[4]] = len(frame)
        arr.append([frame[l[4]],tag[l[3]]])
    elif tagtype == "fre":
        arr.append([frame[l[4]],tag[l[3]]])
    if tagtype == "fle":
        if f1 not in frame:
            frame[f1] = len(frame)
        if f2 not in framer:
            framer[f2] = len(framer)
        arr.append([frame[f1],framer[f2],tag[l[3]]])

if len(arr) - 1 != instance:    sys.exit("ERR: Size Missmatch")
print >> sys.stderr, instance, len(frame)+len(framer), len(tag)
clab = ["0"] * len(tag)

for (ii,r) in enumerate(arr):
    ivec = []
    ivecr = []
    if r == -1:
        print "-1"
        continue
    clab [r[-1]] = "1"
    lab = " ".join(clab)
    ivec.append(str(r[0]))
    print "CLAMP Input ALL SPARSE \n",
    if len(r) == 2:
        vec = " ".join(ivec)
        print vec, ","
    elif len(r) == 3:
        ivecr.append(str(len(frame) + r[1]))
        vec = " ".join(ivec) + " " + " ".join(ivecr)
        print vec, ","
    print "TARGET Output 2 FULL " + lab + "\n;"
    clab[r[-1]] = "0"
