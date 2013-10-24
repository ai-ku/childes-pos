#!/usr/bin/env python

import sys
import math
from scipy.stats import norm
# ./z-test.py mean1 std1 mean2 std2 

def ztest(m1, s1, m2, s2, alpha):
  "two tailed Z-test"
  std = max(s1, s2)
  z = (m1 - m2) / std
  z_norm = norm.cdf(z)
  print z_norm, z
  if z_norm < alpha / 2 or z_norm > 1 - alpha / 2:
    return "True" 
  else:
    return "False" 
    
mean1 = float(sys.argv[1])
std1= float(sys.argv[2])
mean2 = float(sys.argv[3])
std2 = float(sys.argv[4])
print "%g vs %g, z-test: %s" % (mean1, mean2, ztest(mean1, std1, mean2, std2, 0.0001))
print "%g vs %g, z-test: %s" % (mean1, 0., ztest(mean1, std1, 0, 0, 0.0001))
print "%g vs %g, z-test: %s" % (mean2, 0., ztest(mean2, std2, 0, 0, 0.0001))
