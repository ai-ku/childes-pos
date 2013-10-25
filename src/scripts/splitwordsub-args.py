#!/usr/bin/env python

import sys
import re

subsCount = [1, 2, 3, 4, 6, 8, 10, 12, 16, 25, 32, 45, 64]
iters = sys.argv[1]
fold = int(sys.argv[2])
seed = sys.argv[3]
dataName = sys.argv[4]
hiddenRatio = sys.argv[5] 
for (i,s) in enumerate(subsCount,start=1):
    foldId = 0
    for r in range(fold):
        print i, seed, foldId, s, iters, fold, dataName, hiddenRatio
        foldId += 1

