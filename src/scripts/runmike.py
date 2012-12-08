#!/usr/bin/env python

import re
import sys
import os

tags = set(["fre", "fle", "prbi" , "psbi", "apsbi", "aprbi","wordsub"])
print sys.argv[1]
m = re.search("^(.*?)\.(.*?)\.mike\.gz\.info$",sys.argv[1])
if m:
    if m.group(2) in tags:
        for line in open(sys.argv[1]):
            l = line.strip().split()
            if l[0] == ">>>":
                name = m.group(1) + "." + m.group(2)
                cmd = "mike_childes -f " + name + ".mike" + \
                    " -i " + l[2] + " -o " + l[3] + \
                    " >" + name + ".runmk" + \
                    " 2>" + name + ".runmk.err &"
                print cmd
                os.system(cmd)
                break

else:
    print "no match"
