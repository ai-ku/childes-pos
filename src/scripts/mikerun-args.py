#!/usr/bin/env python

import sys
import re

seed = 1
subsCount = [1, 2, 3, 4, 6, 8, 10, 12, 16, 25, 32, 45, 64]
repeat = 10
m = re.search('^(.*?)\.(.*?)$', sys.argv[1])
if not m:
    sys.exit("can not matched the input:{0}".format(sys.argv[1]))
data = m.group(1)
frame = m.group(2)

for (i,s) in enumerate(subsCount,start=1):
    seed = 1
    for r in range(repeat):
        print i,seed,s,data,frame
        seed += 1
