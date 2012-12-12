#!/usr/bin/env python

import sys
import gzip
import re
from itertools import izip

tags = sys.argv[1]
subs = sys.argv[2]
ratio = .30
regLine=re.compile("^L(\d+)")
data = []
sdata = []

for fi in gzip.open(subs):
    fi = fi.strip().split()
    sdata.append(" ".join(fi[1:]))

for fi in open(tags):
    fi = fi.strip().split()
    if fi[0] == "-1":
        data.append(fi[0])
    mm = regLine.search(fi[0])
    if mm:
        sid = int(mm.group(1))
#        print >> sys.stderr, fi[3], mm.group(1), sdata[sid]
        data.append(fi[3] + " " + sdata[sid])



if len(sdata) != len(data) - 1:
    sys.exit("Dimension mismatch: data{0} sdata:{1}\n".format(len(data),len(sdata)))
train = False

for d in data:
    if d == "-1":
        train = True
        continue
    if train:
        print d
    else:
        print >> sys.stderr, d
    
