import re
import os

def rpspace(matched):
    # replace the space in the numbers
    value=str(matched.group('value'))
    return value.replace(" ","")
    
def judgecn(word):
    # judge the word is weather one chinese and all chinese
    # if not all chinese chatacter return false
    for char in word:
        if char<u'\u4e00' or char>u'\u9fff':
            return False
    return True  

def analyzeline(line):
    word=[]
    tags=[]
    # 这个有个问题就是比如90年代这些他本来没有分开的词语并不会分开
    p=re.compile(r'(?P<value>[0-9<]+[0-9|sub|sup|<|>|//|/./ ]+[0-9>%])')
    reline=re.sub(p,rpspace,line)
    # 按照空格进行切分
    thelist=reline.split()
    llen=len(thelist)
    # 对于每一个被分出来的词进行标记
    for oneword in thelist:
        if not judgecn(oneword):
            # 遇到非中文的词组的时候
            word.append(oneword)
            tags.append("S")
            continue
        wlen=len(oneword)
        if wlen==1:
            word.append(oneword)
            tags.append("S")
            continue
        for i in range(wlen):
            word.append(oneword[i])
            if i==0:
                tags.append("B")
                continue
            if i==wlen-1:
                tags.append("E")
                break
            tags.append("M")
    return word,tags

def annyfile(filename):
    # for one file to analyze not one line or string
    f=open(filename,"r",encoding="utf-8")
    lines=f.readlines()
    outlist=[]
    for line in lines:
        outlist.append(analyzeline(line))
    # print(outlist)
    return outlist

filename="train_cws.txt"
annyfile(filename)