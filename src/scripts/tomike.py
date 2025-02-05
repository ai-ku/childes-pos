#!/usr/bin/env python

import sys
import gzip
from collections import defaultdict as dd


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
partition = []
for fi in range(2,len(sys.argv)):
    for line in gzip.open(sys.argv[fi]):
        l = line.strip().split()
        if l[1] == "X":
            continue
        instance += 1
        f1,f2 = l[2].split(":")
        if l[1] not in tag:
            tag[l[1]] = len(tag)
        if tagtype == "pr"  and f1 not in frame:
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
            arr.append([frame[l[2]],tag[l[1]]])
        elif tagtype == "fre":
            arr.append([frame[l[2]],tag[l[1]]])
        if tagtype == "fle":
            if f1 not in frame:
                frame[f1] = len(frame)
            if f2 not in framer:
                framer[f2] = len(framer)
            arr.append([frame[f1],framer[f2],tag[l[1]]])
    partition.append(str(instance))

#print >> sys.stderr, "frame:",len(frame), "right:", len(framer)
#print >> sys.stderr, "tag:"," ".join(tag)
## header
print >> sys.stderr, ">>>", len(arr), len(frame)+len(framer), len(tag), " ".join(partition)
clab = ["0"] * len(tag)
ivec = ["0"] * len(frame)
ivecr = ["0"] * len(framer)
frame = "fre"
for (ii,r) in enumerate(arr):
    if ii % 1000 == 0: print >> sys.stderr, ".",
    clab [r[-1]] = "1"
    lab = " ".join(clab)
    ivec[r[0]] = "1"
    print "CLAMP Input ALL FULL ",
    if len(r) == 2:
        vec = " ".join(ivec)
        print vec
    elif len(r) == 3:
        ivecr[r[1]] = "1"
        vec = " ".join(ivec) + " " + " ".join(ivecr)
        print vec
        ivecr[r[1]] = "0"
    print "TARGET Output 2 FULL " + lab + "\n;"
    ivec[r[0]] = "0"
    clab[r[-1]] = "0"
