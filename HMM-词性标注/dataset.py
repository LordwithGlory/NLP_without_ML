import numpy as np


# 对人工分词文件进行处理，提取出词和对应的词性[[(戴相龙,NR),(word,tag),(,)....],[],[]....]
def data_process(data_file):
    data_list = []
    sentence_list = []
    count=0
    data_file = open(data_file, "r", encoding="utf-8")
    for line in data_file.readlines():
        if '<sub>' in line:
            count+=1
            continue
        elif '<sup>' in line:
            count+=1
            continue
        else:
            lineArr=line.strip().split()
            for i in range(len(lineArr)):
                if(lineArr[i]=='$$__' or lineArr[i]=='$$_'):
                    continue
                else:
                    if "/" not in lineArr[i]:
                        lineArr[i]+="/n"
                    elif "/"==lineArr[i]:
                        lineArr[i]+="/w"
                    word_tuple=tuple(lineArr[i].split('/'))
                    if len(word_tuple)!=2:
                        continue
                    else:
                        sentence_list.append(word_tuple)
                #print(sentence_list)
        data_list.append(sentence_list)
        sentence_list=[]
    print(count)
    return data_list


def creat_matrix(train_data):  # train_data存放所有的训练句子，[[(戴相龙,NR),(,),(,)....],[],[]....]
    tag_dict = {}  # tag_dict存放训练集中所有的tag，及其编号,考虑了起始和终止词性
    word_dict = {}  # word_dict存放训练集中所有的word，及其编号,加入了未知词
    for sentence in train_data:
        for word, tag in sentence:
            if word not in word_dict.keys():
                word_dict[word] = len(word_dict)
            if tag not in tag_dict.keys():
                tag_dict[tag] = len(tag_dict)

    tag_dict['BOS'] = len(tag_dict)
    tag_dict['EOS'] = len(tag_dict)
    #word_dict['???'] = len(word_dict)
    # 将分词和词性以及对应编号以字典形式保存到文件中
    with open("word.dict", "w", encoding="utf-8") as word_dict_file:
        word_dict_file.write(str(word_dict))
    with open("tag.dict", "w", encoding="utf-8") as tag_dict_file:
        tag_dict_file.write(str(tag_dict))
    # 第(i,j)个元素表示词性j在词性i后面的概率（拓展了1行1列，最后一行是start，最后一列是stop）
    transition_matrix = np.zeros([len(tag_dict) - 1, len(tag_dict) - 1])
    # 第(i,j)个元素表示词性i发射到词j的概率
    emission_matrix = np.zeros([len(tag_dict) - 2, len(word_dict)])

    # 计算发射矩阵参数
    alpha = 0.1
    for sentence in train_data:
        for word, tag in sentence:
            emission_matrix[tag_dict[tag]][word_dict[word]] += 1
    for i in range(len(emission_matrix)):
        s = sum(emission_matrix[i])
        for j in range(len(emission_matrix[i])):
            emission_matrix[i][j] = (emission_matrix[i][j] + alpha) / (s + alpha * (len(word_dict)))  # 加alpha平滑

    # 计算转移矩阵参数
    for i in range(len(train_data)):
        for j in range(len(train_data[i]) + 1):
            if j == 0:
                try:
                    transition_matrix[-1][tag_dict[train_data[i][j][1]]] += 1  # 初始tag频率
                except IndexError:
                    continue
            elif j == len(train_data[i]):
                transition_matrix[tag_dict[train_data[i][j - 1][1]]][-1] += 1  # 结束tag频率
            else:
                transition_matrix[tag_dict[train_data[i][j - 1][1]]][tag_dict[train_data[i][j][1]]] += 1

    for i in range(len(transition_matrix)):
        s = sum(transition_matrix[i])
        for j in range(len(transition_matrix[i])):
            transition_matrix[i][j] = (transition_matrix[i][j] + alpha) / (s + alpha * (len(tag_dict) - 1))
    return transition_matrix, emission_matrix

# 对于训练结果转换为测试可以使用的结果
def readFile(filenam):
    # 默认参数readFile("predict.txt")
    inputf=open(filenam,"r",encoding="utf-8")
    outputf=open("lastcixing.txt","w",encoding="utf-8")
    lines=inputf.readlines()
    count=0
    for line in lines:
        thelist=line.split()
        if line=="" or line==None or len(thelist)==0:
            outputf.write("\n")
            count+=1
            continue
        outputf.write(thelist[0]+"/"+thelist[1]+" ")
    outputf.close()
    print(count)

# 对于测试文件中可能出现的问题进行矫正
def corectFile(filename):
    # 默认参数 corectFile("test_posgeshi.txt")
    inputf=open(filename,"r",encoding="utf-8")
    output=open("lastposinput.txt","w",encoding="utf-8")
    lines=inputf.readlines()
    for line in lines:
        if "<sub>" in line or "<sup>" in line:
            continue
        output.write(line)
    output.close()
    
def train_hmm(trainfile):
    train_data = data_process(trainfile)
    #print(train_data)
    transition_matrix, emission_matrix = creat_matrix(train_data)
    np.savetxt("transition_matrix.txt", transition_matrix)
    np.savetxt("emission_matrix.txt", emission_matrix)

