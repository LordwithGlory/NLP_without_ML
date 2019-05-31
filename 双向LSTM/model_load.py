import torch
import gensim
from dataset import *
import time
from model_train import *

# 参数是模型对应文件名称，测试文件文件名称，返回值是预测结果
def load_run(modelname,testname):
    # 参数默认：“"posmodle32.m"”，"test_pos1.txt"，
    model=LSTMTagger(3,3,len(word2id),len(tag2id))
    model.load_state_dict(torch.load(modelname))

    wordlst,taglst=loading_data(testname)
    input=formart_input(wordlst)
    out=model(input)  
    out=out*(-1)
    out=torch.max(out,1)[1]
    print(out)
    myresult=[]
    with torch.no_grad():
        for i in range(0,out.size()[0]):
            findone=out.numpy()[i]
            if id2tag.get(findone):
                myresult.append(id2tag[findone])
            else:
                myresult.append(id2tag.get(findone))
    return myresult

load_run("posmodle32.m","test_pos1.txt")