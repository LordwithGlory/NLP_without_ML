import numpy as np
import os

# 判断是否是一个数字
def jdgdigital(onenum):
    onenum=onenum.replace(".","")
    return onenum.isdigit()

# 将文件内容格式化，输出是得到的word的list以及tag的list
def loading_data(filename):
    wordlst=[]
    taglst=[]
    fr = open(filename,encoding='utf-8-sig',errors='ignore')
    for line in fr.readlines():
        lineArr=line.strip().split()
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
                    taglst.append("/m")
                    continue
                if lineArr[i].isalpha():
                    taglst.append("/nx")
                    continue
                if lineArr[i]=='.':
                    taglst.append("/w")
                    continue
                taglst.append("/nx")
                continue
            wordlst.append(lineArr[i][:wordlen])
            taglst.append(lineArr[i][wordlen+1:])
    return wordlst,taglst

