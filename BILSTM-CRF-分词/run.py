import torch
import os
import torch.autograd as autograd
import torch.nn as nn
import torch.optim as optim
import torch.tensor
import time
from dataset import *
from evaluate import *
from model import *

def writeLine(wordlist,taglist):
    onesen=""
    tempword=""
    for i in range(len(wordlist)):
        tempword+=wordlist[i]
        if taglist[i]=="S" or taglist[i]=="E":
            onesen+=tempword+" "
            tempword=""
    f=open("fencires.txt","a",encoding="utf-8")
    f.write(onesen)
    f.write("\n")
    f.close()

def model_load_run(modlename,testfile):
    # testfile默认参数是test_cws1.txt
    START_TAG = "<START>"
    STOP_TAG = "<STOP>"
    tag_to_ix = {"S": 0, "B": 1, "M": 2, "E":3,START_TAG: 4, STOP_TAG: 5}
    ix_to_tag=["S","B","M","E",START_TAG,STOP_TAG]
    EMBEDDING_DIM = 5
    HIDDEN_DIM = 4
    training_data=annyfile("train_cws.txt")
    word_to_ix = {}
    for sentence, tags in training_data:
        for word in sentence:
            if word not in word_to_ix:
                word_to_ix[word] = len(word_to_ix)
    model=BiLSTM_CRF(len(word_to_ix), tag_to_ix, EMBEDDING_DIM, HIDDEN_DIM)
    model.load_state_dict(torch.load(modlename))
    test_data=annyfile("test2.txt")
    corretNum=0
    predNum=0
    hisNum=0
    with torch.no_grad():
        print("IN TESTING")
        for i in range(len(test_data)):
            # 可能存在未收录的词语，因此对于prepare_sequence进行修改，如果出现未收录词语则认为应当标记为S
            # 存在两种预测方法，用单词预测用字预测
            precheck_sent = prepare_sequence(test_data[i][0], word_to_ix)
            oneline=[ix_to_tag[w] for w in model(precheck_sent)[1]]
            #correnum,prednum,hisnum=cmpletter(test_data[i][1],oneline)
            correnum,prednum,hisnum=cmpline(test_data[i][1],oneline)
            writeLine(test_data[i][0],oneline)
            corretNum=corretNum+correnum
            predNum=prednum+predNum
            hisNum=hisnum+hisNum
    print(corretNum/predNum,corretNum/hisNum)

# 可以在train_model函数中修改训练集默认为train_cws.txt
# modelname=train_model()
# 对于model进行预测
model_load_run("fencinlpmodle99.m","test2.txt")