#!/usr/bin/env python

import sys
import re

seed = 1
frames = ["fle", "fre"]
repeat = 10
it = sys.argv[1]
ratio = sys.argv[2]

for (i,fr) in enumerate(frames,start=1):
    seed = 1
    for r in range(repeat):
        print i,seed,fr,it,ratio
        seed += 1

