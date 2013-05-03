#!/usr/bin/env python

import re,sys,os,argparse

tags = set(["fre", "fle", "prbi" , "psbi", "apsbi", "aprbi","wsub","trws","trfle", "trfre"])
parser = argparse.ArgumentParser(description="Mike-net run script")
parser.add_argument("-iter","-i", type=int, default=10000,help="number of neural-network iterations (default: %(default)s).")
parser.add_argument("-tr", default=None, help="train data-file")
parser.add_argument("-te", default=None, help="test data-file")
parser.add_argument("-info", default=None, help="data info file")
parser.add_argument('-v','-verbose', default = False, help='verbose', action="store_true")
parser.add_argument('-seed', type=int, default = 1, \
                        help='seed value (default: %(default)s)', action="store")
args = parser.parse_args()
iters = args.iter
trainFile=args.tr
testFile = args.te
infoFile = args.info
seed = args.seed
m = re.search("^(.*?)\.(.*?)\.runmk\.info$",infoFile)

if m and m.group(2) in tags:
    with open(infoFile) as inf:
        ll = inf.readline().strip().split()
        datasize, feature, tags= ll
        name = m.group(1) +  "." + m.group(2)
        cmd = "mike_childes -f " + trainFile + \
            " -seed " + str(seed) + \
            " -i " + feature + " -o " + tags + \
            " -v -iter "+ str(iters)+ " -t " +  testFile +" > " + name + ".runmk" + \
            " 2> " + name  + ".runmk.err &"
        if args.v: print "cmd:",cmd
        os.system(cmd)
else:
    sys.exit("Wrong input files")
