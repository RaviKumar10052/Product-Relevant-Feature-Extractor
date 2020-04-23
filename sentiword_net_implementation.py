#!/usr/bin/env python

"""
Interface to SentiWordNet using the NLTK WordNet classes.

---Chris Potts
"""
import tkinter

import re
import os
import sys
import codecs
import nltk
nltk.download('wordnet')

try:
    from nltk.corpus import wordnet as wn
    # from nltk.corpus import sentiwordnet as wn
except ImportError:
    sys.stderr.write("Couldn't find an NLTK installation. To get it: http://www.nltk.org/.\n")
    sys.exit(2)

######################################################################

class SentiWordNetCorpusReader:
    def __init__(self, filename):
        """
        Argument:
        filename -- the name of the text file containing the
                    SentiWordNet database
        """        
        self.filename = filename
        self.db = {}
        self.parse_src_file()

    def parse_src_file(self):
        lines = codecs.open(self.filename, "r", "utf8").read().splitlines()
        lines = filter((lambda x : not re.search(r"^\s*#", x)), lines)
        for i, line in enumerate(lines):
            fields = re.split(r"\t+", line)
            fields = map(str.strip, fields)            #Raghav change unicode to str
            try:            
                pos, offset, pos_score, neg_score, synset_terms, gloss = fields
            except:
                sys.stderr.write("Line %s formatted incorrectly: %s\n" % (i, line))
            if pos and offset:
                offset = int(offset)
                self.db[(pos, offset)] = (float(pos_score), float(neg_score))

    # def senti_synset(self, *vals):
    #     if tuple(vals) in self.db:
    #         pos_score, neg_score = self.db[tuple(vals)]
    #         pos, offset = vals
    #         synset = wn._synset_from_pos_and_offset(pos, offset)
    #         return SentiSynset(pos_score, neg_score, synset)
    #     else:
    #         # print("ceck: " + vals[0])
    #         synset = wn.synset(vals[0])
    #         # print("synset")
    #         pos = synset.pos
    #         offset = synset.offset
    #         if (pos, offset) in self.db:
    #             pos_score, neg_score = self.db[(pos, offset)]
    #             return SentiSynset(pos_score, neg_score, synset)
    #         else:
    #             return None

    def senti_synset(self, *vals):
        from nltk.corpus import wordnet as wn
        if tuple(vals) in self.db:
            pos_score, neg_score = self.db[tuple(vals)]
            pos, offset = vals
            if pos == 's':
                pos = 'a'
            synset = wn._synset_from_pos_and_offset(pos, offset)
            return SentiSynset(pos_score, neg_score, synset)
        else:
            synset = wn.synset(vals[0])
            pos = synset.pos()
            if pos == 's':
                pos = 'a'
            offset = synset.offset()
            if (pos, offset) in self.db:
                pos_score, neg_score = self.db[(pos, offset)]
                return SentiSynset(pos_score, neg_score, synset)
            else:
                return None

    def senti_synsets(self, string, pos=None):
        sentis = []
        synset_list = wn.synsets(string, pos)
        for synset in synset_list:
            # sentis.append(self.senti_synset(synset.name))
            # sentis.append(self.senti_synset(str(synset.name)[37:-3]))
            print("sentimental: ")
            print(synset.name())
            print(wn.synsets(string, pos))
            sentis.append(self.senti_synset(synset.name()))
        # print("check2:")
        # print(sentis)
        sentis = filter(lambda x : x, sentis)
        # print("check3: " + sentis)
        return sentis

    # def senti_synsets(self, string, pos=None):
    #     from nltk.corpus import wordnet as wn
    #     sentis = []
    #     synset_list = wn.synsets(string, pos)
    #     for synset in synset_list:
    #         sentis.append(self.senti_synset(synset.name()))
    #     sentis = filter(lambda x: x, sentis)
    #     return sentis

    def all_senti_synsets(self):
        for key, fields in self.db.items():       #Raghav change iteritems to items
            pos, offset = key
            pos_score, neg_score = fields
            synset = wn._synset_from_pos_and_offset(pos, offset)
            yield SentiSynset(pos_score, neg_score, synset)

######################################################################
            
class SentiSynset:
    def __init__(self, pos_score, neg_score, synset):
        self.pos_score = pos_score
        self.neg_score = neg_score
        self.obj_score = 1.0 - (self.pos_score + self.neg_score)
        self.synset = synset

    def __str__(self):
        """Prints just the Pos/Neg scores for now."""
        s = ""
        s += self.synset.name + "\t"
        s += "PosScore: %s\t" % self.pos_score
        s += "NegScore: %s" % self.neg_score
        return s

    def __repr__(self):
        return "Senti" + repr(self.synset)
                    
######################################################################        



if __name__ == "__main__":
    """
    If run as

    python sentiwordnet.py

    and the file is in this directory, send all of the SentiSynSet
    name, pos_score, neg_score trios to standard output.
    """
    SWN_FILENAME = "SentiWordNet_3.0.0_20130122.txt"
    if os.path.exists(SWN_FILENAME):
        swn = SentiWordNetCorpusReader(SWN_FILENAME)
        for senti_synset in swn.all_senti_synsets():
            pass;
            # print (senti_synset.synset.name, senti_synset.pos_score, senti_synset.neg_score)
