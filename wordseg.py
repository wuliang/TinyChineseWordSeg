#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import codecs
#import pprint

class WordSeg(object):

    def __init__(self):
        self.words=self.init_wordslist()
        self.trie=self.words_2_trie(self.words)

    # No Need to use Regex
    def ngram(self, n, terms):
        for i in xrange(len(terms) - n + 1):
            yield terms[i:i+n]


    def init_wordslist(self, fn="./words.txt"):
        f = codecs.open(fn, 'rt', encoding='utf8')
        lines=sorted(f.readlines())
        f.close()
        return lines


    def words_2_trie(self, wordslist):
        d={}
        for word in wordslist:
            # must remove the last newline
            word = word.strip()
            ref=d
            for char in self.ngram(1, word):
                #print char, word[0]
                ref[char]=ref.has_key(char) and ref[char] or {}
                ref=ref[char]
            ref['']=1
        return d

    def splitTerms(self, chars):
        lst = []
        trie = self.trie
        fail = False
        while len(chars)>=1:
            ref=trie
            index=0
            state=[]
            for char in chars:
                if ref.has_key(char):
                    if ref[char].has_key(""):
                        state.append(index)
                    ref=ref[char]
                else:
                    break
                index += 1
            if not state or state[-1]==0:
                index=1
                if fail:
                    lst.append(lst.pop() + chars[0])
                else:
                    lst.append(chars[0])
                chars=chars[1:]
                fail = True
            else:
                index=state[-1]+1
                lst.append(''.join(chars[:index]))
                chars=chars[index:]
                fail = False
        return lst

def read_testfile(fn="./test.txt"):
    f = codecs.open(fn, 'rt', encoding='utf8')
    lines=f.readlines()
    f.close()
    return lines

def main():
    #pp = pprint.PrettyPrinter(indent=4)

    #init
    seg = WordSeg()
    #pp.pprint(trie)

    #read content
    lines=read_testfile()
    #lines=[u"我爱北京天安门",u"好好打一架钢琴。"]
    for line in lines:
        # better remove the last newline
        line = line.strip()
        result = seg.splitTerms(line)
        print '|'.join(result)

if __name__=='__main__':
    main()



