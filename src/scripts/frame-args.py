#!/usr/bin/env python

import sys
import re

seed = 1
frames = ["fle","pr", "ps","aps","apr", "fre"]
repeat = 10
data = sys.argv[1]
it = sys.argv[2]

for (i,fr) in enumerate(frames,start=1):
    seed = 1
    for r in range(repeat):
        print i,seed,data,fr,it,
        seed += 1
