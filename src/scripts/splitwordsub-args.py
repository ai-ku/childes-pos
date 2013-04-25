#!/usr/bin/env python

import sys
import re

seed = 1
subsCount = [1, 2, 3, 4, 6, 8, 10, 12, 16, 25, 32, 45, 64]
repeat = 10
iters = sys.argv[1]
ratio = sys.argv[2]
data = sys.argv[3]
for (i,s) in enumerate(subsCount,start=1):
    seed = 1
    for r in range(repeat):
        print i,seed,s,iters,ratio, data
        seed += 1

