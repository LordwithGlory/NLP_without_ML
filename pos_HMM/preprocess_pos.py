import numpy as np
import os

def jdgdigital(onenum):
    onenum=onenum.replace(".","")
    return onenum.isdigit()

def loading_data(filename):
    # 第一个里面没两行是一组，第一行是词，第二行是tag
    # tag_set指的是所有词语的tag
    tag_set=set()
    word_set=set()
    train_data=[]
    fr = open(filename,encoding='utf-8-sig',errors='ignore')
    for line in fr.readlines():
        train_data.append(loadline(line,tag_set,word_set))
    # 保存词性的集合到文件中
    f=open("tag_set.txt","w")
    for tag in tag_set:
        f.write(tag)
        f.write("\n")
    f.close()
    # print(tag_set)
    f=open("word_set.txt","w",encoding="utf-8")
    for word in word_set:
        f.write(word)
        f.write("\n")
    f.close()
    # print(word_set)
    return train_data,tag_set,word_set

def loadline(line,tag_set,word_set):
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
            word_set.add(lineArr[i])
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
            word_set.add(lineArr[i])
            wordlst.append(lineArr[i])
            taglst.append("n")
            tag_set.add("n")
            continue
        elif "." in lineArr[i][wordlen+1:]:
            word_set.add(lineArr[i])
            wordlst.append(lineArr[i])
            taglst.append("nx")
            tag_set.add("nx")
            continue
        word_set.add(lineArr[i][:wordlen])
        wordlst.append(lineArr[i][:wordlen])
        taglst.append(lineArr[i][wordlen+1:])
        tag_set.add(lineArr[i][wordlen+1:])    
    return wordlst,taglst

def row_norm(x):
    x.dtype=float
    try:
        x.shape[1]
    except:
        x_max=np.max(x[1])
        x_min=np.min(x[1])
        x=(x-x_min)/(x_max-x_min)
        return x

    for i in range(x.shape[0]):
        x_max=np.max(x[i])
        x_min=np.min(x[i])
        if x_max==x_min:
            x[i]=np.zeros(x[i].shape)
            continue
        x[i]=(x[i]-x_min)/(x_max-x_min)
    return x

def makeMartix(tag_set,train_list,word_set):
    # 对所有taglst进行分析，就是最原始那种全部
    tag_len=len(tag_set)
    tag_dir=dict(zip(list(tag_set),range(tag_len)))
    # 转移矩阵
    trans_matrix=np.zeros((tag_len,tag_len))
    # 词性出现的概率
    cixing_prob=np.zeros(tag_len,dtype=int)
    pre_tag=""
    for i in range(len(train_list)):
        tags=train_list[i][1]
        for tag in tags:
            # 将某个词性出现概率加一
            cixing_prob[tag_dir[tag]]+=1
            if pre_tag=="":
                pre_tag=tag
                continue
            trans_matrix[tag_dir[tag]][tag_dir[pre_tag]]+=1
            pre_tag=tag
    # 进行归一化
    trans_matrix=row_norm(trans_matrix)
    cixing_prob=row_norm(cixing_prob)
    # 保存转移概率和词性概率
    np.savetxt("trans.txt",trans_matrix)
    np.savetxt("cixing.txt",cixing_prob)
    # 建立一个字典，用于word和tag对照
    word_dir=dict(zip(list(word_set),range(len(word_set))))
    # 初始化发射矩阵
    emitter_pro_matrix=np.zeros((len(word_set),len(tag_set)))
    for train_data in train_list:
        sentence=train_data[0]
        tagence=train_data[1]
        for i in range(len(sentence)):
            # 因为我们是一个集合所以大家都有东西 不会没有的
            emitter_pro_matrix[word_dir[sentence[i]]][tag_dir[tagence[i]]]+=1
    emitter_pro_matrix=row_norm(emitter_pro_matrix)
    np.savetxt("fasheMa.txt",emitter_pro_matrix)
