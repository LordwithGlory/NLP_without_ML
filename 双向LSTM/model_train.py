import torch
import gensim
from dataset import *
import time

torch.manual_seed(2)
word1,tag1=loading_data("train_pos.txt")
word2,tag2=loading_data("val_pos.txt")

words=[]
tags=[]
for item in word1:
    words.append(item)
for item in word2:
    words.append(item)
for item in tag1:
    tags.append(item)
for item in tag2:
    tags.append(item)
id2word=gensim.corpora.Dictionary([words])
word2id=id2word.token2id

id2tag=gensim.corpora.Dictionary([tags])
tag2id=id2tag.token2id

def sen2id(inputs):
    # edited!!!
    # regard themost is noun
    # 还必须添加对应的数字来寻找他的属性
    backlist=[]
    for word in inputs:
        if word2id.get(word):
            backlist.append(word2id.get(word))
        else:
            backlist.append(0)
            # if word.isdigit():
            #     backlist.append("m")
            # elif word.isalpha():
            #     backlist.append("nx")
            # # not consider about the "$$_" and "$$__"
            # else:
            #     backlist.append("n")
    return backlist
    #return [word2id.get(word) for word in inputs]

def tags2id(inputs):
    return [tag2id.get(word) for word in inputs]

def formart_input(inputs):
    return torch.autograd.Variable(torch.LongTensor(sen2id(inputs)))

def formart_tag(inputs):
    return torch.autograd.Variable(torch.LongTensor(tags2id(inputs)))

class LSTMTagger(torch.nn.Module):
    def __init__(self,embedding_dim,hidden_dim,voacb_size,target_size):
        super(LSTMTagger,self).__init__()
        self.embedding_dim=embedding_dim
        self.hidden_dim=hidden_dim
        self.voacb_size=voacb_size
        self.target_size=target_size
        self.lstm=torch.nn.LSTM(self.embedding_dim,self.hidden_dim)
        self.log_softmax=torch.nn.LogSoftmax()
        self.embedding=torch.nn.Embedding(self.voacb_size,self.embedding_dim)
        self.hidden=(torch.autograd.Variable(torch.zeros(1,1,self.hidden_dim)),torch.autograd.Variable(torch.zeros(1,1,self.hidden_dim)))
        self.out2tag=torch.nn.Linear(self.hidden_dim,self.target_size)
    def forward(self,inputs):
        input=self.embedding((inputs))
        out,self.hidden=self.lstm(input.view(-1,1,self.embedding_dim),self.hidden)
        tags=self.log_softmax(self.out2tag(out.view(-1,self.hidden_dim)))
        return tags

def trainModel():
# 默认是训练文件有两个 train_pos.txt val_pos.txt
    model=LSTMTagger(3,3,len(word2id),len(tag2id))
    loss_function=torch.nn.NLLLoss()
    #设置model.parameters的学习率为0.1
    optimizer=torch.optim.SGD(model.parameters(),lr=0.1)
    lasttime=time.time()
    for _ in range(100):
        model.zero_grad()
        input=formart_input(word1)
        tags=formart_tag(tag1)
        out=model(input)
        loss=loss_function(out,tags)
        loss.backward(retain_graph=True)
        optimizer.step()
        nowtime=time.time()
        print("The time of"+str(_)+"="+str(nowtime-lasttime))
        lasttime=nowtime
        filename="fenciposmodle"+str(_)+".m"
        # 为了节省时间所以每次训练出一个model都会有一个模型被保存
        torch.save(model.state_dict(),filename)
        #print(loss.item())
    return "fenciposmodle99.m"

