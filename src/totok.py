#!/usr/bin/env python

import sys
    
sent = ""
for l in sys.stdin:
    if not l.strip(): 
        print sent
        sent = ""
        continue
    w , tag = l.strip().split()
    sent += w + " "
    

