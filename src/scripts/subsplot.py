#!/usr/bin/env python2.7 

# Draws the substitute vs accuracy graph with error bars

import sys
import re
import numpy as np
import matplotlib.pyplot as plt

PlotMarks = ['-', '--', '-.', ':', 's--', 'd--']
class childData():
  def __init__(self):
    self.name = None 
    self.sub = []
    self.acc = []
    self.err = []

  def __str__(self):
    assert len(self.sub) == len(self.acc) == len(self.err) 
    rstr = self.name + "\n"
    for s,a,e in zip(self.sub, self.acc, self.err):
      rstr += str(s) + "\t" + str(a) + "\t" + str(e) + "\n" 
    return rstr

def getData():
  datas = []
  for f in sys.stdin:
    c = childData()
    fname = f.strip()
    m = re.search('\/(\w+)\.wsub\.plot$', fname)
    assert m
    c.name = m.group(1)
    for l in open(fname):
      c.name = c.name.split('.')[0]
      sub, acc, err = l.strip().split()
      c.sub.append(float(sub))
      c.acc.append(float(acc))
      c.err.append(float(err))
    datas.append(c) 
  return datas

def substitutePlot(datas, outName="substitute.pdf"):
  plt.figure()
  legend = []
  fsz = 10
  plt.xlim([0, max(datas[0].sub) + 1])
  for (i,c) in enumerate(datas):
    # uncomment for subplot
    #plt.ylim([.70, 1])
    #plt.subplot(len(datas)/2, 2, i + 1)
    #plt.errorbar(c.sub, c.acc, yerr = c.err, fmt=PlotMarks[3]) 
    #plt.legend([c.name], loc='lower right',fontsize=fsz)  
    #uncomment for oneplot
    plt.errorbar(c.sub, c.acc, fmt=PlotMarks[i]) 
    legend.append(c.name)
    # move below into for to get subplot
  plt.legend(legend, loc='lower right',fontsize=fsz)  
  plt.xticks([1,4,8,16,25,32,48,64], fontsize=fsz)
  plt.yticks(fontsize=fsz)
  plt.ylim(ymax = 0.87)
  plt.ylabel("Averaged Accuracy",fontsize=fsz)
  plt.xlabel("Number of Substitutes", fontsize=fsz)
  plt.savefig(outName)

datas = getData()
substitutePlot(datas)
