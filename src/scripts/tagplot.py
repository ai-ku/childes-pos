#!/usr/bin/env python2.7 

# Draws the substitute vs accuracy graph with error bars

import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict as dd 

PlotMarks = ['-', '--', '-.', ':', 's--', 'd--']

def getData():
  datas = dd(lambda: dd(int))
  for f in sys.stdin:
    fname = f.strip()
    child = f.strip().split('.')
    child = child[0].split('/')
    for l in open(fname):
      larr = l.strip().split()  
      if larr[0] != "#":
        datas[child[-1]][larr[0]] = float(larr[1])
  return datas

def tagPlot(datas, outName="tags.pdf"):
  plt.figure()
  legend = []
  fsz = 16
  i = 0
  xorder = ["n", "wh", "adj", "v", "det", "adv", "conj", "prep", "neg", "int"]
  xticks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  for (c, cn) in sorted(datas.items(), key=lambda x: x[0]):
    vals = []
    legend.append(c)
    for n in xorder:
      if n in cn:
        vals.append(cn[n])
      else:
        vals.append(0)
    plt.errorbar(xticks, vals, fmt=PlotMarks[i])
    i += 1
    print c,vals
  plt.xticks(xticks, xorder, fontsize=fsz)
  leg = plt.legend(legend, loc='best', fontsize=fsz - 4, fancybox=True)
  leg.get_frame().set_alpha(0.2)
  plt.yticks(fontsize=fsz)
  plt.ylabel("Averaged Accuracy", fontsize=fsz)
  plt.xlabel("Grammatical Category", fontsize=fsz)
  plt.savefig(outName)
    
datas = getData()
for (n, vn) in datas.items():
  print n
  for (c, vc) in vn.items():
    print c, vc,
tagPlot(datas, sys.argv[1])

