#!/usr/bin/env python


import sys, random,gzip, argparse
from collections import defaultdict as dd
from pprint import pprint as pp

parser = argparse.ArgumentParser(description="Train/test crossvalidate split data")
parser.add_argument('-foldNum', type=int, default=10, \
    help='number of folds (default: %(default)s)', action="store")
parser.add_argument('-tarFold', type=int, default = 0, \
    help='return the required fold (default: %(default)s)', action="store")
parser.add_argument('-seed', type=int, default = 1, \
    help='seed value (default: %(default)s)', action="store")
parser.add_argument('-v','-verbose', default = False, help='verbose', action="store_true")
parser.add_argument('-i','-instanceId', default = False, help='print instance-id after shuffle', action="store_true")
parser.add_argument('-d', '-data', default=None, help='target data file', action="store")
parser.add_argument('-w', '-wordSample', default=False, help='Sample word level (default is sentence level)', action="store_true")

args = parser.parse_args()
seed = args.seed
fold = args.foldNum
dataFile = args.d
foldNumber = args.tarFold
sentenceSample = args.w

if fold <= foldNumber:
  sys.exit("Required fold is greater than number of folds")
sentence = dd(lambda :[])
data = []
di = 0
random.seed(seed)

if args.v:
  print >> sys.stderr, "data:%s seed:%d foldNumber:%d foldTarget:%d"  \
      % (dataFile, seed, fold, foldNumber)
if not dataFile: sys.exit("missing file") 
f = None
if dataFile.endswith('.gz'):
  f = gzip.open(dataFile)
else:
  f = open(dataFile)
with f:
  for line in f:
    line = line.strip()
    l = line.split("\t")
    if l[0] == "##": continue
    data.append(line)
    sentence[l[0]].append(di)
    di += 1

keys = sentence.keys()
random.shuffle(keys)
train, test = [], []
if not sentenceSample:
  # each sentence is sampled to test or train set
  for (i,k) in enumerate(keys):
    if i % fold == foldNumber:
      test.append(sentence[k])
    else:
      train.append(sentence[k])

  for t in test:
    for ins in t:
      if args.i:
        print "L"+str(ins),data[ins]
      else:
        print data[ins]
  print "-1"
  for t in train:
    for ins in t:
      if args.i:
        print "L"+str(ins),data[ins]
      else:
        print data[ins]
else:
  # each word is sampled to test or train set 
  randomIdx = range(len(data))
  random.shuffle(randomIdx)
  for (i,k) in enumerate(randomIdx):
    if i % fold == foldNumber:
      test.append(k)
    else:
      train.append(k)
  for t in test:
    if args.i:
      print "L"+str(t),data[t]
    else:
      print data[t]
  print "-1"
  for t in train:
    if args.i:
      print "L"+str(t),data[t]
    else:
      print data[t]

