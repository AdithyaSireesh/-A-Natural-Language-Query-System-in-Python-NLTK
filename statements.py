# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst, item):
    if (item not in lst):
        lst.insert(len(lst), item)


class Lexicon:
    """stores known word stems of various part-of-speech categories"""

    def __init__(self):
        self.lex = {
            'P': [],
            'N': [],
            'A': [],
            'I': [],
            'T': [],
        }

    def add(self, stem, cat):
        if cat in self.lex:
            if stem not in self.lex[cat]:
                self.lex[cat].append(stem)

    def getAll(self, cat):
        return self.lex[cat]


        # add code here


class FactBase:
    """stores unary and binary relational facts"""

    def __init__(self):
        self.unaryFacts = []
        self.binaryFacts = []

    def addUnary(self, stem1, stem2):
        self.unaryFacts.append((stem1, stem2))

    def addBinary(self, stem1, stem2, stem3):
        self.binaryFacts.append((stem1, stem2, stem3))

    def queryUnary(self, stem1, stem2):
        return (stem1, stem2) in self.unaryFacts

    def queryBinary(self, stem1, stem2, stem3):
        return (stem1, stem2, stem3) in self.binaryFacts
        # add code here


import re
from nltk.corpus import brown

VBZ =[]
VB = []
gold_stand = brown.tagged_words()
for (x,y) in gold_stand:
    if y == 'VBZ':
        VBZ.append(x)
    if y == 'VB':
        VB.append(x)
def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    s_length = len(s)

    if s == 'has':
        return 'have'

    if s not in VBZ:
        return ""

    if re.match("([a-z]|[A-Z])*([^iosxz])es", s) is not None:
        if re.match("([a-z]|[A-Z])*([cs]h)es", s) is None:
            if s[:-1] in VB:
                return s[:-1]

    if re.match("([a-z]|[A-Z])*([^s]se|[^z]ze)s", s) is not None:
        if s[:-1] in VB:
            return s[:-1]

    if re.match("([a-z]|[A-Z])*(o|x|ch|sh|ss|zz)es", s) is not None:
        if s[:-2] in VB:
                return s[:-2]

    if re.match("[^AEIOUaeiou]ies", s) is not None:
        if s[:-1] in VB:
                return s[:-1]

    if s_length>= 5 and re.match("([a-z]|[A-Z])*[^aeiou]ies", s) is not None:
        if (s[:-3] + 'y') in VB:
                return s[:-3] + 'y'

    if re.match("([a-z]|[A-Z])*(a|e|i|o|u)ys", s) is not None:
        if s[:-1] in VB:
                return s[:-1]

    if re.match("([a-z]|[A-Z])*([^sxyzaeiou])s", s) is not None:
        if re.match("([a-z]|[A-Z])*([sc][h])s", s) is None:
            if s[:-1] in VB:
                return s[:-1]

    return ""



def add_proper_name(w, lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w, 'P')
        return ''
    else:
        return (w + " isn't a proper name")


def process_statement(lx, wlist, fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name(wlist[0], lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a', 'an']):
                lx.add(wlist[3], 'N')
                fb.addUnary('N_' + wlist[3], wlist[0])
            else:
                lx.add(wlist[2], 'A')
                fb.addUnary('A_' + wlist[2], wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add(stem, 'I')
                fb.addUnary('I_' + stem, wlist[0])
            else:
                msg = add_proper_name(wlist[2], lx)
                if (msg == ''):
                    lx.add(stem, 'T')
                    fb.addBinary('T_' + stem, wlist[0], wlist[2])
    return msg

# End of PART A.