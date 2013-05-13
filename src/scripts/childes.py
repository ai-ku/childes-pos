#!/usr/bin/env python

import sys
from lxml import etree
from lxml import objectify
from pprint import pprint as pp 

class childes:
    class sentence:
        def __init__(self, sid = None, who = None):
            self.id = sid
            self.who = who
            self.type = ""
            self.content = []
            self.error = False
        def append(self,w):
            self.content.append(w)
        def __str__(self):
            out = "[sentence %s %s %s %s]\n" % (str(self.id), str(self.who),\
                                                    str(self.type), str(self.error))
            for w in self.content:
                out += w.__str__() + "\n"
            return out
        def __iadd__(self,stc):
            if stc.id == None or (stc.id == self.id):
                self.content += stc.content
            else:
                print >> sys.stderr, "Bug in Sentence.__iadd_ %s" % self.id
            return self
    class word:
        def __init__(self, w = "", c = "", s = "", stem = ""):
            self.w, self.c, self.s = w, c, s
            self.stem = stem
            self.type = ""
            self.pfx = ""
            self.composite = False
            self.replacement = False
            self.repeat = 1
        def __str__(self):
            out = "w:" + str(self.w) + "\tc:" + str(self.c) + \
                "\ts:" + str(self.s) +"\tst:"+str(self.stem) + \
                "\tpfx:" + str(self.pfx) + "\ttype:" + str(self.type) +\
                "\tcomposite:"+str(self.composite) + "\treplacement:" + str(self.replacement)
            for i in range(self.repeat - 1):
                out += "\n[r]" + out
            return out

    def __init__(self, fileName):
        self.tagDict = {"part":"Participants", "sent":"u", "word":"w", \
                        "mor":"mor", "short":"shortening", "punc":"t", \
                            "g":"g", "comma":"tagMarker", "pause":"pause",\
                            "senType":"k", "overlap":"overlap", "composite":"wk",\
                            "replacement":"replacement", "error":"error",\
                            "fragment":"fragment", "fragTag":"p", "repeat":"r"
                            }
        self.parser = etree.XMLParser(ns_clean=True)
        self.fileName = fileName
        self.root = None
        self.participants = {}
        self.sentences = []
        self.current = None
        if self.fileName:
            self.root = self.parse().getroot()

    def parse(self):
        return etree.parse(self.fileName, self.parser)

    def __str__(self):
        return etree.tostring(self.root, pretty_print = True)

    def print_node(self, elm):
        print etree.tostring(elm, pretty_print = True)

    def get_data(self):
        for p in self.root:
            tag = p.xpath("local-name()")
            if tag == self.tagDict["part"]:
                self.get_participants(p)
            elif tag == self.tagDict["sent"]:
                self.get_sentence(p)
            else:
                print "skip",tag

    def get_participants(self, elm):
        print "participants:",
        for p in elm:
            if p.get("role").find("Child") == -1:
                self.participants[p.get("id")] = p.get("role")
        print self.participants

    def get_sentence(self, elm):
        if elm.get("who") not in self.participants:
            print >> sys.stderr, "[skip sentence %s, %s]" % (elm.get("who"), elm.get("uID"))
            return
#        if elm.get("uID") != "u795":
#            return
        self.current = self.sentence(sid=elm.get("uID"), who=elm.get("who"))
        self.get_tags(elm, self.current)
        print self.current
        self.current = None

    def get_tags(self,elm, stc = None):
        if not stc:
            stc = self.sentence()
        for p in elm:
            tag = p.xpath("local-name()")
            if tag == self.tagDict["word"]:
                rw = self.get_word(p)
                if rw.__class__.__name__ == "word":
                    stc.append(rw)
                elif rw.__class__.__name__ == "sentence":
                    stc += rw
            elif tag == self.tagDict["punc"] or tag == self.tagDict["comma"]:
                stc.append(self.get_punc(p))
            elif tag == self.tagDict["g"]: ##[!!] what does g mean???
                gStc = self.get_tags(p)
                stc += gStc
            #### Helper Tags
            elif tag == self.tagDict["repeat"]:
                for w in stc.content:
                    w.repeat = int(p.get("times"))
            elif tag == self.tagDict["error"]:
                stc.error = True
            elif tag == self.tagDict["pause"]:
                ptype = "P_" + p.get("symbolic-length")
                stc.append(self.word(w=ptype, c = ptype, s = ptype))
            elif tag == self.tagDict["senType"]: ##[!!] what does g mean???
                stc.type += p.get("type")
            elif tag == self.tagDict["overlap"]: ##[!!] what does g mean???
                stc.type += p.get("type")
            else:
                if tag not in set(["a","e", "linker", "quotation", "ga", "postcode"]): 
                    print >> sys.stderr, "unhandled\t%s\t%s\t%s" % \
                        (self.current.id, "get_tags", tag)
        return stc

    def get_punc(self, elm):
        ptype = "P_" + elm.get("type")
        curw = self.word(w=ptype, c = ptype, s = ptype)
        return curw

    def get_word(self, elm):
        curw = self.word(w=elm.text) if elm.text != None  else self.word()
        if elm.get("type") != None: curw.type = elm.get("type")
        for p in elm:
            tag = p.xpath("local-name()")
            if tag == self.tagDict["mor"]:
                self.get_morph(p, curw)
            elif tag == self.tagDict["short"]:
                curw.w += p.text + p.tail if p.tail != None else p.text
            elif curw.type == self.tagDict["fragment"] and tag == self.tagDict["fragTag"]:
                curw.w += p.tail if p.tail != None else ""
                if p.get("type") != None: curw.type += "_" + p.get("type")
            elif tag == self.tagDict["replacement"]:
                curw = self.get_tags(p)
                for c in curw.content:
                    c.replacement = True
            elif tag == self.tagDict["composite"]:
                curw.w += "_" + p.tail
                curw.composite = True
            else:
                print >> sys.stderr, "unhandled\t%s\t%s\t%s" % \
                    (self.current.id, "get_word", tag)
        return curw
    def get_replacement(self, elm):
        for p in elm:
            tag =  p.xpath("local-name()") 
            if tag == self.tagDict["word"]:
                curw = self.get_word(p)
            else:
                print >> sys.stderr, "unhandled\t%s\t%s\t%s" % \
                    (self.current.id, "get_replacement", tag)
            curw.replacement = True
            return curw
        
    def get_morph(self, elm, word = None):
        for p in elm:
            tag =  p.xpath("local-name()") 
            if tag == "mw":
                self.get_mw(p,word)
            elif tag == "mwc":
                if word.composite:#compound words with "cmp"
                    self.get_mw(p,word)
                else: #compound words without "cmp" in <w>
                    word.composite = True
                    self.get_mw(p,word)
            else:
                ##[!!] handle mor-post to handle tokens such as it's
                if tag not in set(["gra", "mor-post", "men-x"]): 
                    print >> sys.stderr, "unhandled\t%s\t%s\t%s" % \
                    (self.current.id, "get_morph", tag)

    def get_mw(self, elm, word = None):
        for p in elm:
            tag = p.xpath("local-name()")
            if  tag == "pos":
                self.get_pos(p,word)
            elif tag == "stem":
                word.stem = p.text
            elif tag == "mpfx":
                word.pfx = p.text
            else:
                if tag not in set(["mk", "mw"]):  #due to compound words
                    print >> sys.stderr, "unhandled\t%s\t%s\t%s" % \
                        (self.current.id, "get_mw", tag)

    def get_pos(self, elm, word = None):
        for p in elm:
            tag = p.xpath("local-name()")
            if  tag == "s":
                word.s = p.text
            elif tag  == "c":
                word.c = p.text
            else:
                print >> sys.stderr, "unhandled:%s:%s:%s" % \
                    (self.current.id, "get_pos", tag)
        
if __name__ == "__main__":
    c = childes(sys.argv[1])
    c.get_data()
#    c.get_participants()
#    c.get_sentence()
