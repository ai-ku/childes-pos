#!/usr/bin/env python

import sys
import re

iters = sys.argv[1]
fold = int(sys.argv[2])
seed = sys.argv[3]
dataName = sys.argv[4]
hiddenRatio = sys.argv[5] 
foldId = 0
for r in range(fold):
  print seed, foldId, iters, fold, dataName, hiddenRatio
  foldId += 1
