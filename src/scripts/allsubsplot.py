#!/usr/bin/env python2.7 

# Draws the substitute vs accuracy graph with error bars

import sys
import re
import numpy as np
import matplotlib.pyplot as plt

PlotMarks = ['-', '--', '-.', ':', 's--', 'd--']
def getData():
  datas = {} 
  cname = ''
  for l in sys.stdin:
    larr = l.strip().split()
    if len(larr) == 2:
      datas[larr[0]] = {'sub':[], 'acc':[], 'err':[]}
      cname = larr[0]
      continue
    sub, acc, err = larr
    datas[cname]['sub'].append(float(sub))
    datas[cname]['acc'].append(float(acc))
    datas[cname]['err'].append(float(err))
  return datas

def substitutePlot(datas, outName="allsubstitute.pdf"):
  plt.figure()
  legend = []
  fsz = 10
  for (i,c) in enumerate(sorted(datas.keys())):
    # uncomment for subplot
    #plt.ylim([.70, 1])
    #plt.subplot(len(datas)/2, 2, i + 1)
    #plt.errorbar(c.sub, c.acc, yerr = c.err, fmt=PlotMarks[3]) 
    #plt.legend([c.name], loc='lower right',fontsize=fsz)  
    #uncomment for oneplot
    sub = datas[c]['sub']
    acc = datas[c]['acc']
    err = datas[c]['err']
    plt.xlim([0, max(sub) + 1])
    plt.errorbar(sub, acc, fmt=PlotMarks[i]) 
    legend.append(c)
    # move below into for to get subplot
  plt.legend(legend, loc='lower right',fontsize=fsz)  
  plt.xticks([1,4,8,16,25,32,48,64], fontsize=fsz)
  plt.yticks(fontsize=fsz)
  plt.ylim(ymax = 0.87)
  plt.ylabel("Accuracy",fontsize=fsz)
  plt.xlabel("Number of Substitutes", fontsize=fsz)
  plt.savefig(outName)

datas = getData()
substitutePlot(datas)
