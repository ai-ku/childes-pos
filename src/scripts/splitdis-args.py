#!/usr/bin/env python

import sys
import re

iters = sys.argv[1]
fold = int(sys.argv[2])
seed = sys.argv[3]
dataName = sys.argv[4]
hiddenRatio = sys.argv[5] 
foldId = 0
nsub = [10, 100, 1000, 2000, 4000]

for s in nsub: 
  seed = sys.argv[3]
  for r in range(fold):
    print seed, foldId, iters, fold, dataName, s, hiddenRatio
  foldId += 1
