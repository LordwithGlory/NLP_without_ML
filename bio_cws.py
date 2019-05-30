#分词后的短语做token
import os
import numpy as np


def txt_loading(filename,datalst):
    lineArr=[]
    count = 0
    new_count = 0
    re=['——','$$_']
    fr = open(filename ,encoding='utf-8',errors='ignore')
    f = open('bmes_cws_tuple.txt','w+',encoding='utf-8',errors='ignore')
        # 对于某行进行特判
        if count == 937 or count ==6059:
            pass
        else:
            new_count+=1
            line = line.strip()
            lineArr = line.split(' ')
            length = len(lineArr)
            tagArr=[]
            new_lineArr=[]
            for i in range(length):
                if is_Chinese(lineArr[i]):
                    wordArr = lineArr[i]
                    end = len(wordArr)
                    if end == 1 or wordArr.isdigit() :
                        tagArr.append('S')
                        new_lineArr.append(wordArr)
                    elif wordArr in re:
                        tagArr.append('S')
                        new_lineArr.append(wordArr)
                    else:
                        for j in range(end):
                            if j == 0:
                                tagArr.append('B')
                            elif j == end-1 :
                                tagArr.append('E')
                            else:
                                tagArr.append('M')
                            new_lineArr.append(wordArr[j])
                    
                else:
                    tagArr.append('S')
                    new_lineArr.append(lineArr[i])
        
            cws_line_tag=(new_lineArr,tagArr)
            datalst.append(cws_line_tag)
            f.write(str(cws_line_tag)+',')
            #f.write(str(tagArr)+'\n')
        
            #print(new_lineArr)
            #print(tagArr)
        """
        生成一个元组
        """
    return datalst,new_count

def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

datalst=[]
datalst,new_count=txt_loading('train_cws.txt',datalst)
print(new_count)

        
