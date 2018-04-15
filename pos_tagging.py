# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:
from statements import *
function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'), 
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    dic = {}
    with open("sentences.txt", "r") as f:
        for line in f:
            #print (line)
            groups = line[:-1].split(' ')
            #print (groups)
            for group in groups:
                w_c = group.split('|')
                #print (w_c)
                if w_c[1] == 'NN' or w_c[1] == 'NNS':
                    if w_c[0] not in dic:
                        dic.update({w_c[0]: [w_c[1]]})
                    else:
                        if w_c[1] not in dic[w_c[0]]:
                            dic[w_c[0]].append(w_c[1])

        #print (dic)
    unchanged_plurals = []
    for word in dic.keys():
        if len(dic[word]) == 2:
            unchanged_plurals.append(word)
        #print (unchanged_plurals)
    return unchanged_plurals


            # add code here

unchanging_plurals_list = unchanging_plurals()
#unchanging_plurals_list

def noun_stem(s):
    """extracts the stem from a plural noun, or returns empty string"""
    s_length = len(s)

    if s in unchanging_plurals_list:
        return s

    if s[-3:] == "men":
        return s[:-3] + "man"

    if re.match("([a-z]|[A-Z])*([^iosxz])es", s) is not None:
        if re.match("([a-z]|[A-Z])*(sh|ch)es", s) is None:
            return s[:-1]
    if re.match("([a-z]|[A-Z])*([^s]se|[^z]ze)s", s) is not None:
        return s[:-1]

    if re.match("([a-z]|[A-Z])*(o|x|ch|sh|ss|zz)es", s) is not None:
        return s[:-2]

    if re.match("[^AEIOUaeiou]ies", s) is not None:
        return s[:-1]

    if s_length>= 5 and re.match("([a-z]|[A-Z])*[^aeiou]ies", s) is not None:
        return s[:-3] + 'y'

    if re.match("([a-z]|[A-Z])*(a|e|i|o|u)ys", s) is not None:
        return s[:-1]

    if re.match("([a-z]|[A-Z])*([^sxyzaeiou])s", s) is not None:
        if re.match("([a-z]|[A-Z])*(sh|ch)s", s) is None:
            return s[:-1]

    return ""
    # --THIS IS THE OLD CODE---
    # s_length = len(s)


    # if re.match(r"([a-z]|[A-Z])*([^sxyzaeiou])s", s) != None:
    #     if re.match(r"([a-z]|[A-Z])*[^sc][^h]s", s) != None:
    #         return s[:-1]
    #
    #
    # if re.match(r"([a-z]|[A-Z])*(a|e|i|o|u)ys", s) != None:
    #     return s[:-1]
    #
    #
    # if s_length >= 5 and re.match(r"([a-z]|[A-Z])*[^aeiou]ies", s) != None:
    #     return s[:-3] + 'y'
    #
    #
    # if re.match(r"[^AEIOUaeiou]ies", s) != None:
    #     return s[:-1]
    #
    #
    # if re.match(r"([a-z]|[A-Z])*(o|x|ch|sh|ss|zz)es", s) != None:
    #     return s[:-2]
    #
    #
    # if re.match(r"([a-z]|[A-Z])*([^s]se|[^z]ze)s", s) != None:
    #     return s[:-1]
    # return ""
    # add code here

def tag_word(lx, wd):
    """returns a list of all possible tags for wd relative to lx"""
    word_tags = []
    pos_tags = [
        'P',
        'N',
        'A',
        'I',
        'T',
    ]
    #for tags in lx.getAll():
    if wd in lx.getAll('P'):
        word_tags.append('P')
    if wd in lx.getAll('A'):
        word_tags.append('A')
    noun = noun_stem(wd)
    if wd in lx.getAll('N') or noun in lx.getAll('N'):
        if noun == "":
            word_tags.append('Ns')
        elif wd == noun:
            word_tags.append('Ns')
            word_tags.append('Np')
        else:
            word_tags.append('Np')
    verb = verb_stem(wd)
    if wd in lx.getAll('I') or verb in lx.getAll('I'):
        if verb == "":
            word_tags.append('Ip')
        else:
            word_tags.append('Is')
    if wd in lx.getAll('T') or verb in lx.getAll('T'):
        if verb == "":
            word_tags.append('Tp')
        else:
            word_tags.append('Ts')

    for (word, tag) in function_words_tags:
        if word == wd:
            word_tags.append(tag)
            break
    return word_tags
    #if noun_stem(wd) != "":
    #    tags.append('NN')
    #for tag in pos_tags:
    #    if wd in lx.getAll(tag):
    #        word_tags.append(tag)
    # add code here

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.


"""print noun_stem("fly")
print noun_stem("flies")
print noun_stem("ducks")
print noun_stem("dogs")
print noun_stem("bathes")
print noun_stem("analyses")
print noun_stem("goes")
print noun_stem("dies")"""