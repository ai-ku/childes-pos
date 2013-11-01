#!/usr/bin/env python

import sys
import numpy as np
from collections import defaultdict as dd
from pprint import PrettyPrinter as pp
import random
# print the accuracy, lambda_a, lambda_b values
# read file list from standard input 
# each file is double column where left column is the gold tags and right
# column is the guessed tags 
# sample run:
# ls aran.wsub16.fold*.out | ./accuracy.pl

def lambdaCalc(total, data, dataT, debug=False):
  # calculate answ|gold lambda_b
  rowMax = max([sum(r.values()) for r in dataT.values()]) 
  maxColSum = sum([max(r.values()) for r in data.values()]) 
  if tot - rowMax != 0:
    lambda_b = (maxColSum - rowMax) / (tot - rowMax)
  else:
    lambda_b = 0
  if debug:
    print "rowMax:", rowMax, " maxColSum:", maxColSum , " N:", tot
    print "data:"
    for g,v in data.items():
      print g, "=>",
      for a, c in v.items():
        print a,c,
      print
    print "dataT"
    for g,v in dataT.items():
      print g, "=>",
      for a, c in v.items():
        print a,c,
      print
  return lambda_b

lambda_b = []
lambda_a = []
acc = []
for f in sys.stdin:
  fname = f.strip()
  cor, tot = 0,0
  data = dd(lambda: dd(int))
  dataT = dd(lambda: dd(int))
  for l in open(fname):
    larr = l.strip().split()
    if len(larr) != 2:
      print >> sys.stderr, "each line of answer file should be two tokens"
      sys.exit(-1)
    elif larr[0] == larr[1]:
      cor += 1
    # gold set is given
    # uncommenting this should produce zero lambda_b
    # larr[1] = random.randint(0,1) 
    data[larr[1]][larr[0]] += 1.
    # answer is given
    dataT[larr[0]][larr[1]] += 1.
    tot += 1.
  acc.append(cor*1.0/tot)  
  lambda_b.append(lambdaCalc(tot, data, dataT))
  lambda_a.append(lambdaCalc(tot, dataT, data))
#  print fname, acc[-1], lambda_b[-1], lambda_a[-1] 
print "all acc %g %g lambda_b %g %g lambda_a %gi %g" % (np.mean(acc), np.std(acc), 
    np.mean(lambda_b), np.std(lambda_b),
    np.mean(lambda_a), np.std(lambda_a))
