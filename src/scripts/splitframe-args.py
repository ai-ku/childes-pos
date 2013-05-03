#!/usr/bin/env python

import sys
import re

frames = ["fle", "fre", "ps", "pr"]
iters = sys.argv[1]
fold = int(sys.argv[2])
seed = sys.argv[3]
dataName = sys.argv[4]

for (i,fr) in enumerate(frames,start=1):
    foldId = 0
    for r in range(fold):
        print i, seed, foldId, fr, iters, fold,dataName
        foldId += 1
