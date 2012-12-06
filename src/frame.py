#!/usr/bin/python
# update: Sun Nov 11 15:57:02 EET 2012

import sys
import re
from itertools import izip
from optparse import OptionParser
from pprint import pprint
from collections import defaultdict as dd

class frame:
    def __init__(self):
        self.data = []
        self.tag = []
        self.types = dd(int)
        self.frameType = 'fre'
        self.frames = dd(lambda: dd(int))
        self.threshold = 45 #remove frames lower < threshold (default top45)
        self.tokenCount = 0
        self.utteranceCount = 0
        self.debug = 1
        self.filterFrameCount = 0
        self.filterUtterBound = False
        self.removeUtterBound = False
        self.filterTokenTags = False
#        self.tagMap={'n':'n','pro':'n','adj':'adj', 'adv':'adv','conj':'conj',\
#                         'det':'det', 'qn':'det', 'prep':'prep', 'v':'v', 'aux':'v',\
#                         'part':'v', 'mod':'v', 'neg':'neg', \
#                         'co':'int', 'int':'int', 'wh':'wh'}
        self.tagMap={'n':'n', 'pro':'n', 'adj':'adj', 'adv':'adv', 'conj':'conj', 'det':'det',\
                          'prep':'prep', 'v':'v', 'aux':'v','int':'int',\
                         'neg':'neg', 'wh':'wh'}
        #### regs ###
        self.regUtterBound = re.compile('^P_')
        self.regWordTag = re.compile('^(.*?)\/(.*?):')
        self.regWhTag = re.compile('^.*?\/.*?:wh:')
        self.regNoTag = re.compile('^(.*?)\/_?$')

    def get_frequent_frames(self):
        for (s,t) in izip(self.data, self.tag):
            if len(s) >= 3:
                for i in range(1,len(s)-1):
                    if self.filterUtterBound and (self.regUtterBound.search(s[i-1]) or self.regUtterBound.search(s[i + 1]) or self.regUtterBound.search(s[i])): continue
                    tt = t[i]
                    if self.filterTokenTags and tt not in self.tagMap:
                        continue
                    elif tt in self.tagMap:
                        tt = self.tagMap[t[i]]
                    pair = (s[i-1],s[i+1])
                    self.frames[pair][(s[i],tt)] += 1
                    self.frames[pair]["_A_"] += 1
            else:
                 continue
        if (self.debug == 1): print >> sys.stderr, "## Frequent-Frames: {0}".format(len(self.frames))

    def get_prebigram_frames(self):        
        for (s,t) in izip(self.data, self.tag):
            if len(s) >= 2:
                for i in range(1,len(s)):
                    if self.filterUtterBound and (self.regUtterBound.search(s[i-1]) or  self.regUtterBound.search(s[i])): continue
                    pair = (s[i-1], "X")
                    tt = t[i]
                    if self.filterTokenTags and tt not in self.tagMap:
                        continue
                    elif tt in self.tagMap:
                        tt = self.tagMap[t[i]]
#                    print "PPP", pair
                    self.frames[pair][(s[i],tt)] += 1
                    self.frames[pair]["_A_"] += 1
            else:
                 continue
        if (self.debug == 1): print >>sys.stderr, "## preBigramFrames: {0}".format(len(self.frames))

    def get_postbigram_frames(self):
        for (s,t) in izip(self.data, self.tag):
            if len(s) >= 2:
                for i in range(len(s)-1):
#                    if s[i+1] == "Aran": print >> sys.stderr, s[i], s[i+1]
                    if self.filterUtterBound and (self.regUtterBound.search(s[i + 1]) or  self.regUtterBound.search(s[i])): continue
                    pair = ("X", s[i+1])
                    tt = t[i]
                    if self.filterTokenTags and tt not in self.tagMap:
                        continue
                    elif tt in self.tagMap:
                        tt = self.tagMap[t[i]]
                    self.frames[pair][(s[i], tt)] += 1
                    self.frames[pair]["_A_"] += 1
            else:
                 continue
        if (self.debug == 1): print >> sys.stderr, "## postBigramFrames: {0}".format(len(self.frames))
            
    def category_accuracy(self, cat):
        hit, total = 0, cat["_A_"] * (cat["_A_"] - 1) * 0.5
        d = dd(int)
        for w,c in cat.items():
            if w == "_A_": continue
            tt = w[1]
            if self.filterTokenTags and tt not in self.tagMap: 
                continue
            elif tt in self.tagMap:
                tt = self.tagMap[tt]               
            d[tt] += c
        ss = sum(map(lambda x: x * (x - 1) * 0.5, d.values()))
        if ss == total and total == 0: return 0
        else: return ss / total

    def filter_frames(self):
        rem = []
        for (i,f) in enumerate(sorted(self.frames.iteritems(), key=lambda x: x[1]["_A_"], reverse=True), start=0):
            if f[1]["_A_"] <= self.filterFrameCount:
                rem.append(f[0])
        for f in rem:
            del self.frames[f]
        if (self.debug == 1): print >> sys.stderr, "## Filtered Frequent-Frames(<= {0}) {1}".\
                format(self.filterFrameCount, len(self.frames))
                    
    def frame_print(self):
        analysedToken, analysedType = 0,{}
        for (i,f) in enumerate(sorted(self.frames.iteritems(), key=lambda x: x[1]["_A_"], reverse=True), start=0):
            if self.threshold == 0 or i < self.threshold: 
                print "{0}:{1}\t{2} acc:{3}\t===>\t".format(f[0][0],f[0][1], f[1]["_A_"], self.category_accuracy(f[1])),
                for (w,c) in sorted(f[1].items(), key=lambda x: x[1], reverse=True):
                    if w == "_A_": continue
                    print "({0},{1}):{2}\t".format(w[0],w[1],c),
                    analysedToken += c
                    analysedType[w] = 1
                print
        print >> sys.stderr, "## Analysed Token:{0} ({1}/{2})".format(1.0 * analysedToken / self.utteranceCount, analysedToken,self.utteranceCount)
        print >> sys.stderr, "## Analysed Type:{0} ({1}/{2})".format(1.0 * len(analysedType) / len(self.types),len(analysedType), len(self.types))

    def cluster_print(self):
        analysedToken, analysedType = 0,{}
        for (i,f) in enumerate(sorted(self.frames.iteritems(), key=lambda x: x[1]["_A_"], reverse=True), start=0):
            if self.threshold == 0 or i < self.threshold:
                cluster = ":".join(f[0])
#                print "{0}:{1}\t{2}\t===>\t".format(f[0][0],f[0][1], f[1]["_A_"]),
                for (w,c) in sorted(f[1].items(), key=lambda x: x[1], reverse=True):
                    if w == "_A_" : continue
                    tt = w[1]
                    analysedToken += c
                    analysedType[w] = 1
                    for i in range(c):
                        if tt in self.tagMap:
                            tt = self.tagMap[tt]
                        else:
                            tt = 'X'
                        print "{0}\t{1}\t{2}".format(w[0],tt,cluster)
        print >> sys.stderr, "## Analysed Token:{0} ({1}/{2})".format(1.0 * analysedToken / self.utteranceCount, analysedToken,self.utteranceCount)
        print >> sys.stderr, "## Analysed Type:{0} ({1}/{2})".format(1.0 * len(analysedType) / len(self.types),len(analysedType), len(self.types))

    def read(self):
        for line in sys.stdin:
            l = line.strip().split()
            self.tokenCount += len(l)
            new_l, new_p = [],[]
            for u in l:
                m = self.regUtterBound.search(u)
                if m == None:
                    self.utteranceCount += 1
                    (w,t) = self.split_tag_word(u.strip())
#                    if w == "going" or w == "doing" or w == "putting": t = 'v'
                    new_l.append(w)
                    self.types[w] += 1
                    new_p.append(t)
                elif self.removeUtterBound and self.regUtterBound.search(u):
                    continue
                else:
#                    self.types[] += 1
                    new_l.append(u)
                    new_p.append(None)
            if new_l:
                if len(new_l) != len(new_p): 
                    print >> sys.stderr, "Shift between words:{0} tags{1} arrays".format(len(new_l),len(new_p))
                    sys.exit(-1)
                self.data.append(new_l)
                self.tag.append(new_p)

    def split_tag_word(self,t):
        m = self.regWordTag.search(t)
        if m == None:
            no = self.regNoTag.search(t)
            if no != None:
#                print >> sys.stderr, "notag", t
                return (no.group(1), "_NOTAG_")
            else:
                print >> sys.stderr, "missing word/tag",t            
                return None
        else:
            wh = self.regWhTag.search(t)
            if wh == None:
                return (m.group(1), m.group(2))
            else:
                return (m.group(1), "wh")

    def get_frames(self):
        if self.frameType == 'fre':
            self.get_frequent_frames()
        elif self.frameType == 'prbi':        
            self.get_prebigram_frames()
        elif self.frameType == 'psbi':
            self.get_postbigram_frames()
        else: ## Default is frequent frames
            self.get_frequent_frames()

    def info(self):
        print >> sys.stderr, "## Sentence:{0} token:{1} utterance:{2} type:{3}".format(len(self.data),\
                                                                                           self.tokenCount,\
                                                                                           self.utteranceCount,\
                                                                                           len(self.types))
        
if __name__ == '__main__':
    usage = "usage: %prog [options] < std-in"
    parser = OptionParser(usage)
    parser.add_option("-f", "--frame_type", action="store", default= 'fre',dest="frame", help="frame types:fre, prbi or psbi. [default: %default]")
    parser.add_option("-t", type="int", dest="thr", default= '45', help="Calculates the top thr frames. [default: %default]")
    parser.add_option("-u", action="store_true", default=False, dest="ufilter", help="filter utterance boundaries (ex:P_*) [defaut: %default]")
    parser.add_option("-m", action="store_true", dest="mintz", help="Clear data according to Mintz(2003) ")
    parser.add_option("-p", action="store_true", default=False, dest="pFrames", help="Print top t frames [default: %default]")
    parser.add_option("-g", action="store_true", default=False, dest="pGroups", help="Print induced groupings (format: word*TAB*gold_tag*TAB*induced_tag) [default: %default]")
    parser.add_option("-r", action="store_true", default=False, dest="filterTags", help="Filter tags that are not in standard gold tag set (Mintz 2003) [default: %default]")
    parser.add_option("-c", type="int", default=1, dest="filterCount", help="Filter frames that are observed less than count [default: %default]")
    (options, args) = parser.parse_args(sys.argv);
    ff = frame()
    if options.thr != None:
        ff.threshold = options.thr
    if options.ufilter != None:
        ff.filterUtterBound = options.ufilter
    if options.mintz != None:
        ff.removeUtterBound = options.mintz
    if options.filterTags != None:
        ff.filterTokenTags = options.filterTags
    if options.frame != None:
        ff.frameType = options.frame
    ff.read()
    ff.info()
    ff.get_frames()
    if options.filterCount != None:
        ff.filterFrameCount = options.filterCount
        #ff.filter_frames()
    if options.pFrames:
        ff.frame_print()
    if options.pGroups:
        ff.cluster_print()
