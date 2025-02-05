#!/usr/bin/env python

import sys
import gzip
from collections import defaultdict as dd


frame = dd(int)
framer = dd(int)
tag = dd()
arr = []
tagtype = "fre"

if sys.argv[2] == "pr":
    tagtype = "pr"
elif sys.argv[2] == "ps":
    tagtype = "ps"
elif sys.argv[2] == "fle":
    tagtype = "fle"

for line in gzip.open(sys.argv[1]):
    l = line.strip().split()
    if l[1] == "X":
        continue
    f1,f2 = l[2].split(":")
    if f1 == "X" or  f2 =="X":
        sys.exit("Wrong frame construction")
    if l[1] not in tag:
        tag[l[1]] = len(tag)
    if tagtype == "pr" and f1 not in frame:
        frame[f1] = len(frame)
        arr.append([frame[f1],tag[l[1]]])
    elif tagtype == "pr":
        arr.append([frame[f1],tag[l[1]]])
    if tagtype == "ps" and f2 not in frame:
        frame[f2] = len(frame)
        arr.append([frame[f2],tag[l[1]]])
    elif tagtype == "ps":
        arr.append([frame[f2],tag[l[1]]])
    if tagtype == "fre" and l[2] not in frame:
        frame[l[2]] = len(frame)
    elif tagtype == "fre":
        arr.append([frame[l[2]],tag[l[1]]])
    if tagtype == "fle":
        if f1 not in frame:
            frame[f1] = len(frame)
        if f2 not in framer:
            frame[f2] = len(framer)
        arr.append([frame[f1],framer[f2],tag[l[1]]])

print >> sys.stderr, "frame:",len(frame), "right:", len(framer)
print >> sys.stderr, "tag:"," ".join(tag)
## header
print len(arr), len(frame)+len(framer), len(tag)
clab = ["0"] * len(tag)
ivec = ["0"] * len(frame)
ivecr = ["0"] * len(framer)
frame = "fre"

for r in arr:
    clab [r[-1]] = "1"
    lab = " ".join(clab)
    ivec[r[0]] = "1"
    if len(r) == 2:
        vec = " ".join(ivec)
        print vec, "\n", lab
    elif len(r) == 3:
        ivecr[r[1]] = "1"
        vec = " ".join(ivec) + " " + " ".join(ivecr)
        print vec, "\n", lab
        ivecr[r[1]] = "0"
    ivec[r[0]] = "0"
    clab[r[-1]] = "0"
