#!/usr/bin/env python2.7 

# Draws the substitute vs accuracy graph with error bars

import sys
import re
import numpy as np
import math
import matplotlib.pyplot as plt
from collections import defaultdict as dd

PlotMarks = ['-', '--', '-.', ':', 's--', 'd--']

def getData():
  datas = dd(list)
  errs = dd(list)
  for s in sys.stdin:
    s = s.strip()
    for l in open(s):
      l = l.strip().split()
      datas[l[0]].append(float(l[1]))
      errs[l[0]].append(float(l[2]))
  return datas, errs 

def substitutePlot(datas, errs, outName="data.pdf"):
  fig = plt.figure()
#  plt.xscale("log")
  legend = []
  fsz = 10
  sizes = map(math.log, [100000, 250000, 500000, 1300000])
#  plt.xlim([0, max(datas[0].sub) + 1])
  for (i,c) in enumerate(datas.keys()):
    # uncomment for subplot
    #plt.ylim([.70, 1])
    #plt.subplot(len(datas)/2, 2, i + 1)
    #plt.errorbar(c.sub, c.acc, yerr = c.err, fmt=PlotMarks[3]) 
    #plt.legend([c.name], loc='lower right',fontsize=fsz)  
    #uncomment for oneplot
    plt.errorbar(sizes, datas[c], fmt=PlotMarks[i]) 
    legend.append(c)
    # move below into for to get subplot
  plt.legend(legend, loc='lower right',fontsize=fsz)  
  plt.xticks(sizes, ['100K', '250K', '500K', '1.3M'], fontsize=fsz)
  plt.yticks(fontsize=fsz)
  plt.ylim(ymin = 0.75, ymax = 0.84)
  plt.xlim(xmin = 11.4, xmax = math.log(1500000))
  plt.ylabel("Accuracy",fontsize=fsz)
  plt.xlabel("Number of Sentences", fontsize=fsz)
  plt.savefig(outName)

datas, errs = getData()
substitutePlot(datas, errs)
