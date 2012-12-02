#!/usr/bin/env python

import sys
import math

for l in sys.stdin:
    line = l.strip().split()
    s = 0
    for i in range(1,len(line)):
        if i % 2 == 0:
            s += pow(10, float(line[i]))
    for i in range(1,10):
        if i % 2 == 0:
            print line[i-1], pow(10,float(line[i]))/s,
    print
