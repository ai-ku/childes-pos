#!/usr/bin/env python

import sys
import re
import gzip
# This script maps the idx of answers and fold gold tags to
# the actual surface form of the tag
# ./idx2tag.py [gold_file] [fold_answer]

# gold_file
# input:
# word_idx word tag [substitutes]
# fold_answer
# gold_idx answer

goldTags = []
words = []
for l in gzip.open(sys.argv[1]):
  larr = l.strip().split()
  words.append(larr[1]) 
  goldTags.append(larr[2]) 

goldIdx = []
ansIdx = []
for l in open(sys.argv[2]):
  l = l.strip()
  if(re.search('^\d+ \d+$', l)):
    larr = l.split()
    goldIdx.append(larr[0])   
    ansIdx.append(larr[1])
  else:
    print >> sys.stderr, l

if len(goldIdx) != len(goldTags):
   print "Mismatch! mikenet test input %d and ouput %d" % (len(goldTags), len(goldIdx))
   sys.exit()

tdict = {} 
for g,idx in zip(goldTags, goldIdx):
  if g not in tdict:
    tdict[idx] = g

for g,a in zip(goldIdx, ansIdx):
  if g in tdict and a in tdict:
    print "%s\t%s" % (tdict[g], tdict[a])
  elif g in tdict:
    print "%s\t%s" % (tdict[g], a)
    print >> sys.stderr, "MISSING_IN_GOLD: goldIdx:%s ansIdx:%s" % (g,a)
  else:
    print >> sys.stderr, "BUG: goldIdx:%s ansIdx:%s" % (g,a)
