import torch
import gensim
from preprocess_pos import *
torch.manual_seed(2)

word1,tag1=loading_data("train_pos.txt")
word2,tag2=loading_data("val_pos.txt")
"""
datas=[('你 叫 什么 名字 ?','n v n n f'),('今天 天气 怎么样 ?','n n adj f'),]
words=[ data[0].split() for data in datas]
tags=[ data[1].split() for data in datas]
"""

id2word1=gensim.corpora.Dictionary([word1])
id2word2=gensim.corpora.Dictionary([word2])
word2id1=id2word1.token2id
word2id2=id2word2.token2id

id2tag1=gensim.corpora.Dictionary([tag1])
id2tag2=gensim.corpora.Dictionary([tag2])
tag2id1=id2tag1.token2id
tag2id2=id2tag2.token2id

def sen2id(inputs):
    word2id=[]
    for word in inputs:
        if word2id1.get(word):
            word2id.append(word2id1[word])
        else:
            word2id.append(word2id2.get(word))
    return word2id

def tags2id(inputs):
    tag2id=[]
    for tag in inputs:
        if tag2id1.get(tag):
            tag2id.append(tag2id1[tag])
        else:
            tag2id.append(tag2id2.get(tag))
    return tag2id

def formart_input(inputs):
    # torch.LongTensor这个方法并不成功
    return torch.autograd.Variable(torch.Tensor(sen2id(inputs)))
        
def formart_tag(inputs):
    return torch.autograd.Variable(torch.LongTensor(tags2id(inputs)),)

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

model=LSTMTagger(3,3,len(word2id1),len(tag2id1))
loss_function=torch.nn.NLLLoss()
#设置model.parameters的学习率为0.1
optimizer=torch.optim.SGD(model.parameters(),lr=0.1)
for _ in range(100):
    model.zero_grad()
    input=formart_input(word1)
    tags=formart_tag(tag1)
    out=model(input)
    loss=loss_function(out,tags)
    loss.backward(retain_graph=True)
    optimizer.step()
    #print(loss.item())

wordlst,taglst=loading_data("test_pos1.txt")
input=formart_input(wordlst)
out=model(input)  
print(out)
out=torch.max(out,1)[1]
print(out)
print(out.numpy()[1])
print(out.data[1].items())
print(out.data[2].items())
print(type(out.data[0]))
#print(out.data[1].eval())
myresult=[]
for i in range(0,out.size()[0]):
    findone=out.numpy()[i]
    if id2tag1.get(findone):
        myresult.append(id2tag1[findone])
    else:
        myresult.append(id2tag2.get(findone))
print(myresult)
#print([id2tag.get(1) for i in range(0,out.size()[0])])
