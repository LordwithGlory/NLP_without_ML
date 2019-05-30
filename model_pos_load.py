import torch
import gensim
from preprocess_pos import *
import time
from pos_train_0530 import *

model=LSTMTagger(3,3,len(word2id),len(tag2id))
model.load_state_dict(torch.load("posmodle32.m"))

wordlst,taglst=loading_data("test_pos1.txt")
# with torch.no_grad():
#     for word in wordlst:
#         mytags=torch.tensor(sen2id(word), dtype=torch.long)
#         print(model(mytags))
f = open("posresult","a",encoding="utf-8")
input=formart_input(wordlst)
# print(input)
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
print(myresult)