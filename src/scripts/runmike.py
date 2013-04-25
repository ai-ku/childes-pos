#!/usr/bin/env python

import re
import sys
import os

seed = 0
tags = set(["fre", "fle", "prbi" , "psbi", "apsbi", "aprbi","wordsub","trws","trfle", "trfre"])
iters = sys.argv[2]
testData = ""

if len(sys.argv) == 4:
    testData = " -t " + sys.argv[3]

m = re.search("^(.*?)\.(.*?)\.mike\.gz\.info$",sys.argv[1])

if m:
    if m.group(2) in tags:
        for line in open(sys.argv[1]):
            l = line.strip().split()
            if l[0] == ">>>":
                name = m.group(1) + "." + m.group(2)
                datasize = l[1]
                cmd = "mike_childes -f " + name + ".mike.gz" + \
                    " -seed " + str(seed) + \
                    " -i " + l[2] + " -o " + l[3] + \
                    " -v -iter "+ iters+ testData+" >" + name + ".runmk" + \
                    " 2>" + name + ".runmk.err &"
                print "cmd:",cmd
                os.system(cmd)
                break

else:
    print "no match"
