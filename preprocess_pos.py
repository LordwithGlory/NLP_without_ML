import numpy as np
import os

re = ['$$_']
tag_set=set()
def jdgdigital(onenum):
    onenum=onenum.replace(".","")
    return onenum.isdigit()

def loading_data(filename):
    train_data=[]
    fr = open(filename,encoding='utf-8-sig',errors='ignore')
    for line in fr.readlines():
        train_data.append(loadline(line))
    return train_data,tag_set

def loadline(line):
    wordlst=[]
    taglst=[]
    lineArr=line.strip().split()
    # 对于空格的处理是不管不问
    for i in range(len(lineArr)):
        if(lineArr[i]=="$$__" or lineArr[i]=="$$_"):
            continue
        wordlen=len(lineArr[i])-1
        try:
            while lineArr[i][wordlen]!="/":
                wordlen=wordlen-1
        except IndexError:
            wordlst.append(lineArr[i])
            if jdgdigital(lineArr[i]):
                taglst.append("m")
                tag_set.add("m")
                continue
            if lineArr[i].isalpha():
                taglst.append("nx")
                tag_set.add("nx")
                continue
            if lineArr[i]=='.':
                taglst.append("w")
                tag_set.add("w")
                continue
            # 例如CO2等都是经过实验的，发现剩余的几乎都是英文混合
            taglst.append("nx")
            tag_set.add("nx")
            continue
        # 少加一个taglst的变化晚睡半小时系列==
        if ">" in lineArr[i][wordlen+1:]:
            wordlst.append(lineArr[i])
            taglst.append("n")
            tag_set.add("n")
            continue
        elif "." in lineArr[i][wordlen+1:]:
            wordlst.append(lineArr[i])
            taglst.append("nx")
            tag_set.add("nx")
            continue
        wordlst.append(lineArr[i][:wordlen])
        taglst.append(lineArr[i][wordlen+1:])
        tag_set.add(lineArr[i][wordlen+1:])    
    return wordlst,taglst