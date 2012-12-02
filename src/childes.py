#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import re
import os
import codecs
from pprint import pprint


class ChildesReader:
#Comman tags
# dictionary data structure of header
    def __init__(self):
        self.headerInfo = {}
        self.participantInfo = {}
        self.speakerTiers = []
        self.outputTxt = []
        self.outputMor = []
        self.participantTag = u"@Participants:"
    # Regular experession of cha files
        self.regHeader = re.compile(u'^(@[\w:]+)(.*)$')
        self.regSpeaker = re.compile(u'^\*(.*?):[\s]*(.*)$')
        self.regDependent = re.compile(u'^%(.*?):[\s]*(.*)$')
        self.regSkip = re.compile(u'^\s*([&\.,!\?;]|cm\|cm|\(\d\.\)|0)\s*$')
        self.regAssimilation = re.compile(u'(\S+)[ ]*\[:(.*?)\]') #word [:correct_form_of_word] => correct_form_of_word
        self.regOverlap = re.compile(u'<(.*?)>[ ]*\[[<|>]\d*?\]') #(<word> or word) ([<] or [>]) or ([<\d] or [>\d]) => word
        self.regBestGuess = re.compile(u'<(.*?)>[ ]*\[\?\]') #word [?]or <word>[?] => word
        self.regErrorMissing = re.compile(u'0*?(\S+)\s*\[\*\]') #0word [*] or word [*] => word
        self.regRepetition = re.compile(u'(<[^<>]+>|\S+)\s*\[\/\]') # word [\] or <word> [\] => remove word or <word>
        self.regRetracing = re.compile(u'(<[^<>]+>|\S+)\s*\[//\]') # word [\\] or <word> [\\] => remove word or <word>
        self.regQuotationFollows = re.compile(u'(\+"\.\s*$|^[\s]*(\+"\s+)+|\+"\.[\s]*)')
        self.regQuotationPrecedes = re.compile(u'\+"\.\s*')
        self.regInterruption = re.compile(u'(\+/\.$|^\+,)')
        self.regSelfCompletion = re.compile(u'^[\s]*\+,')
        self.regContrastiveStress = re.compile(u'<([^<>]+)>[\s]*\[!!\]')  #word [!!]or <word>[!!] => word
        self.regStressing = re.compile(u'<([^<>]+)>[\s]*\[!!\]')  #word [!]or <word>[!] => word
        self.regParalinguistic = re.compile(u'<([^<>]+)>[\s]*\[=[!?]*\s*.*?\]') #word or <word> [=[?!] word]
        self.regParalinguisticZero = re.compile(u'0[\s]*\[=[!?]*\s*.*?\]') #word or <word> [=[?!] word]
#        self.regAlternativeTranscrion = re.compile(u'<(.*)>[\s]*\[=?\s*.*?\]') 
        self.regSQuotaSpace = re.compile(u'“(\w)');
        self.regEQuotaSpace = re.compile(u'(\w)”');
        self.regLayzOverlap = re.compile(u'\+<');
        self.regDualOverLapRetracing = re.compile(u'<[^<>]+>\s*\[[<>\?\!]\]\s*\[//?\]');
        self.regDualOverLapRetracingWord = re.compile(u'\S+\s*\[[<>\?\!]\]\s*\[//?\]');
        self.regCommentOnMainLine = re.compile(u'\[% .*?\]') # [% word] => removes
        self.regActionTire = re.compile(u'\[%act:\s* .*?\]')
        self.regRemoveStrangeSym = re.compile(u'\.*?\')
        self.regCorrectWord = re.compile(u'\((\w+)\)')
        self.regChildesTags = re.compile(u'(\(\.+\)|w{3}|x{2,3}|y{2,3}|&\S+|\[=[!?]*\s*[^\]\[]+\]|\[\* .*?\])|\[[<|>]\d*\]|\+(//|//\?)|\[!{1,2}\]|\[\?\]|^[ ]*\+\+|\[x \d+\]|\[\+ \S+]|^\+\^')
    def  __clear__(self):
        self.headerInfo = {}
        self.participantInfo = {}
        self.speakerTiers = []
        self.outputTxt = []
        self.outputMor = []

    def get_participants(self):
        part = []    
        if self.headerInfo.get(self.participantTag):
            val = self.headerInfo[self.participantTag].split(',')
            for p in val:
                pm = re.search(u'^[\s]*(.*?)[\s]+(.*?)$', p)
                (ptag, pval) = pm.group(1), pm.group(2)
                self.participantInfo[ptag] = pval

    def get_text_participant(self, tag):
        for po in self.speakerTiers:
            if po["tag"] == tag:
                pprint(po["txt"])

    def get_gold_tags(self, tag):
    #should we split this regexps?
        for po in self.speakerTiers:
            if po["tag"] != tag:
                txt,mor = po["txt"], ""
                if po.get("mor"):             
                    mor = po["mor"]
                    otxt = txt
                    # two level
                    txt = self.regDualOverLapRetracing.sub("",txt)
                    txt = self.regDualOverLapRetracingWord.sub("",txt)
                    # one level
                    txt = self.regOverlap.sub(ur'\1',txt)
                    txt = self.regAssimilation.sub(ur'\2',txt)
                    txt = self.regBestGuess.sub(ur'\1',txt)
                    txt = self.regErrorMissing.sub(ur'\1',txt)
                    txt = self.regRepetition.sub("",txt)
                    txt = self.regRetracing.sub("",txt)
                    txt = self.regContrastiveStress.sub(ur'\1',txt)
                    txt = self.regStressing.sub(ur'\1',txt)
                    txt = self.regQuotationFollows.sub("",txt)
                    mor = self.regQuotationFollows.sub("",mor)
                    txt = self.regQuotationPrecedes.sub("",txt)
                    mor = self.regQuotationPrecedes.sub("",mor)
                    txt = self.regSelfCompletion.sub("",txt)
                    txt = self.regParalinguistic.sub(ur'\1',txt)
                    txt = self.regParalinguisticZero.sub("",txt)
                    txt = self.regSQuotaSpace.sub(ur'bq \1',txt)
                    txt = self.regEQuotaSpace.sub(ur'\1 eq',txt)
                    txt = self.regCommentOnMainLine.sub("",txt)
                    txt = self.regActionTire.sub("",txt)
                    txt = self.regLayzOverlap.sub("",txt)
                    txt = self.regCorrectWord.sub(r'\1',txt)
                    txt = self.regChildesTags.sub("",txt) #always the last one
                    mor = self.regChildesTags.sub("",mor) #always the last one
                    txt = txt.strip()
                    mor = mor.strip()
                    txtArr = txt.split()
                    morArr = mor.split()
                    pair = []
                    txtArr = filter(lambda x: self.regSkip.match(x) == None, txtArr)
                    morArr = filter(lambda x: self.regSkip.match(x) == None, morArr)
                    if len(morArr) != len(txtArr):
                        print >> sys.stderr, u"[Original]",otxt
                        print >> sys.stderr, u"[Modified]",txt
                        print >> sys.stderr, len(morArr), morArr
                        print >> sys.stderr, len(txtArr), txtArr
#                        print >> sys.stderr,u"[mor]", mor
                        pair = self.tag_matcher(txtArr, morArr)                    
                        print >> sys.stderr, u"[pair]", pair
                        print >> sys.stderr
                    else:
                        #                    pair = tag_matcher(txtArr, morArr)
                        #                    print "CORRECT", pair
                        self.outputTxt.append(txtArr)
                        self.outputMor.append(morArr)

## Word-tag matcher
    def tag_matcher(self, txtA, morA):
        m = 0
        pair = []
        for t in txtA:
            if not self.regSkip.match(t):
                if m == len(morA): break;
                pair.append((t,morA[m]))
                m += 1
        return pair
    

    def read_cha(self, fileName):
## Object is participant tag => 
##            'TXT' => text of participant 
##            'MOR' => morphology of text        
        currentParObj = {}
        interruptionObj = {}
        lastest=""
        for line in codecs.open( fileName, "r", "utf-8" ): # open(fileName):
            # problems related to file system (I guess)
            line = self.regRemoveStrangeSym.sub("", line)            
            m = self.regHeader.search(line)
    ## Can we do better?
            if  m:
                self.headerInfo[m.group(1)] = m.group(2)
                self.get_participants()
                continue
            m = self.regSpeaker.search(line)
            if m:
                latest="txt"
                if re.search(ur'^\+"?,',m.group(2)) and interruptionObj.get(m.group(1)) != None:
#                    print >> sys.stderr, "Interruption continues", line
                    currentParObj = interruptionObj[m.group(1)]
                    currentParObj["txt"] += re.sub(ur'(^\+|(\+\/\.|\+\.\.\.)[\s]*$)', "",m.group(2));
#                    currentParObj["txt"] += re.sub(ur'^\+,', "",m.group(2));
                else:
#                    print  >> sys.stderr, "No interruption continues", line, interruptionObj
                    interruptionObj[m.group(1)] = None
                    currentParObj = {}
                    currentParObj["tag"] = m.group(1)
                    currentParObj["txt"] = m.group(2)
                self.speakerTiers.append(currentParObj)
                if re.search(ur'(\+/\.|\+\.\.\.)\s*$',m.group(2)) and interruptionObj.get(m.group(1)) == None:                   
                    interruptionObj[m.group(1)] = currentParObj;
                    currentParObj["txt"] = re.sub(ur'(\+\/\.|\+\.\.\.)[\s]*$', "",m.group(2));
#                    print >> sys.stderr, "Interruption start:",line
#                else:
#                    print >> sys.stderr, "No Interruption:",line
#                    interruptionObj[m.group(1)] = None
                continue
            m = self.regDependent.search(line)
            if m:
                if currentParObj == None: print >> sys.stderr, "Null object error"
                latest = m.group(1)
                if currentParObj.get(m.group(1)):
                    currentParObj[m.group(1)] += re.sub(ur'(\+\/\.|\+\.\.\.)[ ]*$', "",m.group(2));
                else:
                    currentParObj[m.group(1)] = re.sub(ur'(\+\/\.|\+\.\.\.)[ ]*$', "",m.group(2));
            if re.search('^\t',line):
                line = line.strip()
                currentParObj[latest] += " " + re.sub(ur'(\+\/\.|\+\.\.\.)[ ]*$', "",line);

    def print_output(self, info):
        for p in range(len(self.outputTxt)):
            for i in range(len(self.outputTxt[p])):
                if info == "txt":
                    print self.outputTxt[p][i],
                elif info == "mor":
                    print self.outputMor[p][i],
                elif info == "txt/mor":
                    print u"{0}\t{1}".format(self.outputTxt[p][i],self.outputMor[p][i])
                else:
                    print u"{0}\t{1}".format(self.outputTxt[p][i],self.outputMor[p][i])
            print

#    def read_directory(self, path):
path = sys.argv[1]
if os.path.isfile(path):
    test = ChildesReader()
    test.read_cha(sys.argv[1])
    test.get_gold_tags("CHI")
    test.print_output("")
else:
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if re.search(ur'^\w*\.cha$',filename):
                fname = os.path.join(dirname, filename)
                print >> sys.stderr, "[FILE]", fname
                child = ChildesReader()
                child.read_cha(fname)
                child.get_gold_tags("CHI")
                child.print_output("txt/mor")




