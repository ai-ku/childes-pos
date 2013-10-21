#!/usr/bin/env python2.7 

# Draws the substitute vs accuracy graph with error bars

import sys
import re
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict as dd 

PlotMarks = ['-', '--', '-.', ':', 's--', ',']
class childData():
  def __init__(self):
    self.name = None 
    self.sub = []
    self.acc = []
    self.err = []
    self.ngram = []

  def __str__(self):
    assert len(self.sub) == len(self.acc) == len(self.err) 
    rstr = self.name + "\t" + str(self.ngram) + "\n"
    for s,a,e in zip(self.sub, self.acc, self.err):
      rstr += str(s) + "\t" + str(a) + "\t" + str(e) + "\n" 
    return rstr

def getAccData():
  datas = dd(lambda: dd(int)) 
  for f in sys.stdin:
    fname = f.strip()
    for l in open(fname):
      larr = l.strip().split()  
      if len(larr) == 3:
        c.sub.append(float(larr[0]))
        c.acc.append(float(larr[1]))
        c.err.append(float(larr[2]))
        datas[c.name][c.ngram] = c
      elif len(larr) == 1:
        larr = l.strip().split('.')
        if len(larr) == 3:
          c = childData()
          m = re.search('\.(\d+)gram$', fname)
          c.name = larr[0]
          assert m
          c.ngram = int(m.group(1))
  return datas

def ngramPlot(datas, outName="ngram.pdf"):
  plt.figure()
  legend = []
  fsz = 14
  i = 0
  for (c, cn) in sorted(datas.items(), key=lambda x: x[0]):
    xticks = []
    vals = []
    err = []
    legend.append(c)
    for (n, vn) in cn.items():
      xticks.append(n)
      vals.append(vn.acc[0])
      err.append(vn.err[0])
    plt.errorbar(xticks, vals, fmt=PlotMarks[i])
    i += 1
    print c,vals,err
  plt.xticks([2,3,4,5], fontsize=fsz)
  plt.legend(legend, loc='lower right',fontsize=fsz)  
  plt.yticks(fontsize=fsz)
  plt.ylabel("Averaged Accuracy",fontsize=fsz)
  plt.xlabel("n-gram order", fontsize=fsz)
  plt.savefig(outName)
    
datas = getAccData()
#for (n, vn) in datas.items():
#  for (c, vc) in vn.items():
#    print vc
ngramPlot(datas)
