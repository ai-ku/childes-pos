#!/usr/bin/env python

import sys
import re

seed = 1
frames = ["fle","pr", "ps","aps","apr", "fre"]
repeat = 10
data = sys.argv[1]

for (i,fr) in enumerate(frames,start=1):
    seed = 1
    for r in range(repeat):
        print i,seed,data,fr
        seed += 1
