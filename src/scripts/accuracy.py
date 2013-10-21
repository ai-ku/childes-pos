#!/usr/bin/env python

import sys
from collections import defaultdict as dd
from pprint import PrettyPrinter as pp
import random

def lambdaCalc(total, data, dataT, debug=False):
  # calculate answ|gold lambda_b
  rowMax = max([sum(r.values()) for r in dataT.values()]) 
  maxColSum = sum([max(r.values()) for r in data.values()]) 
  lambda_b = (maxColSum - rowMax) / (tot - rowMax)
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

cor, tot = 0,0
data = dd(lambda: dd(int))
dataT = dd(lambda: dd(int))

for l in open(sys.argv[1]):
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

lambda_b = lambdaCalc(tot, data, dataT)
lambda_a = lambdaCalc(tot, dataT, data)

print cor * 1.0 / tot, lambda_b, lambda_a 
