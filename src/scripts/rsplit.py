#!/usr/bin/env python


import sys
import random
import gzip
from collections import defaultdict as dd
ratio = .30
sentence = dd(lambda :[])
random.seed(sys.argv[1])
if len(sys.argv) == 5:
    ratio = float(sys.argv[4])
data = []
di = 0
for line in open(sys.argv[2]):
    line = line.strip()
    l = line.split()
    if l[0] == "##": continue
    data.append(line)
    sentence[l[0]].append(di)
    di += 1
thr = int(len(sentence)*ratio)
frames = [line.strip() for line in gzip.open(sys.argv[3]) if line]
if len(data) != len(frames): sys.exit("size mismatch data:{0} frames:{1}\n".format(len(data),len(frames)))
keys = sentence.keys()
random.shuffle(keys)
for (i,k) in enumerate(keys):
    if thr and i > thr:
        print >> sys.stderr,"-1"
        print "-1"
        thr = 0
    for ins in sentence[k]:
        print >> sys.stderr, "L"+str(ins),data[ins]
        print frames[ins] 

#print len(data),len(data)-thr, thr
