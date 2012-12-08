#!/usr/bin/env python

import sys
    
sent = ""
for line in sys.stdin:
    l = line.strip().split()
    if l[0]  == "##":
        continue
    else:
        stcid = l[0]
        wid = int(l[1])
        wtag = l[2]
        l = l[3:]
        if l[wid] != "X":
            sys.stderr("Missing taget word:{0} {1}".format(l[wid]," ".join(l)))
        else:
            print " ".join(l)


