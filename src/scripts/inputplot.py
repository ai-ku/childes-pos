#!/usr/bin/env python2.7
import numpy as np
import matplotlib.pyplot as plt

n_children = 6

means_par= (4999.3, 6066.3, 4261.1, 3366.3, 4936.3, 4290.5)
std_par = (39.86, 40.84, 32.18, 39.11, 36.29, 34.56)

means_syn = (3601, 4857, 2928, 2396, 3084,2835)

fig, ax = plt.subplots()

index = np.arange(n_children)
bar_width = 0.35

opacity = 0.8
error_config = {'ecolor': '0'}

plt.bar(index, means_syn, bar_width,
    alpha=opacity,
    color='r',
    error_kw=error_config,
    label='aX+Xb')

plt.bar(index + bar_width, means_par, bar_width,
    alpha=opacity,
    color='b',
    yerr=std_par,
    error_kw=error_config,
    label='a*b')

plt.xlabel('Child Corpus')
plt.ylabel('Number of Input Units')
#plt.title('Scores by group and gender')
xticksLabel = ('Anne', 'Aran', 'Eve', 'Naomi', 'Nina', 'Peter') 
plt.xticks(index + bar_width, xticksLabel) 
plt.legend()
plt.tight_layout()
#plt.show()
plt.savefig("inputlayer.pdf")
