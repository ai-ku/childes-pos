#!/usr/bin/env python2.7 

# Draws the substitute vs accuracy graph with error bars

import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict as dd 

PlotMarks = ['-', '--', '-.', ':', 's--', 'd--']
def getAccData():
  datas = dd(lambda: dd(float))
  for f in sys.stdin:
    fname = f.strip()
    pflag = False
    data, ngram = "dummy", 0
    for l in open(fname):
      larr = l.strip().split()  
      if not pflag and len(larr) == 3:
        data = larr[0] 
        ngram = larr[2]
        pflag = True
      elif pflag:
        #ppl idx:5 ppl1 idx: 7
        datas[data][ngram] = float(larr[5])
        pflag = False
  return datas

def ngramPlot(datas, outName="perplexity.pdf"):
  plt.figure()
  legend = []
  fsz = 14
  i = 0
  for (c, cn) in sorted(datas.items(), key=lambda x: x[0]):
    xticks = []
    vals = []
    err = []
    legend.append(c)
    for (n, vn) in sorted(cn.items(), key=lambda x: x[0]):
      xticks.append(n)
      vals.append(vn)
    plt.errorbar(xticks, vals, fmt=PlotMarks[i])
    i += 1
    print c,vals,err
  plt.xticks([2,3,4,5], fontsize=fsz)
  plt.legend(legend, loc='best',fontsize=fsz)  
  plt.yticks(fontsize=fsz)
  plt.ylabel("Perplexity",fontsize=fsz)
  plt.xlabel("n-gram order", fontsize=fsz)
  plt.savefig(outName)
    
datas = getAccData()
#for (n, vn) in datas.items():
#  for (c, vc) in vn.items():
#    print n,c,vc
ngramPlot(datas) 
