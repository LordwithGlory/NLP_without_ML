import torch
import os
import torch.autograd as autograd
import torch.nn as nn
import torch.optim as optim
import torch.tensor
import time
from preprocess_pos import *
from train_CIXING import BiLSTM_CRF,argmax,prepare_sequence,log_sum_exp

START_TAG = "<START>"
STOP_TAG = "<STOP>"
EMBEDDING_DIM = 5
HIDDEN_DIM = 4

# Make up some training data
training_data=[]
training_data,tags_set = loading_data('train_pos.txt')
# 字典用于对应词性和数字标记
tag_to_ix={}
tags_set_num=0
for onetag in tags_set:
    tag_to_ix[onetag]=tags_set_num
    tags_set_num=tags_set_num+1
tag_to_ix[START_TAG]=len(tag_to_ix)
tag_to_ix[STOP_TAG]=len(tag_to_ix)
word_to_ix = {}
for sentence, tags in training_data:
    for word in sentence:
        if word not in word_to_ix:
            word_to_ix[word] = len(word_to_ix)
model=BiLSTM_CRF(len(word_to_ix), tag_to_ix, EMBEDDING_DIM, HIDDEN_DIM)
model.load_state_dict(torch.load("cixingnlpmodle0.m"))
test_data,_=loading_data("test_pos1.txt")
ix_to_tag={v:k for k,v in tag_to_ix.items()}
with torch.no_grad():
    oneline=[]
    for i in range(len(test_data)):
        precheck_sent = prepare_sequence(test_data[i][0], word_to_ix)
        oneline.append([ix_to_tag[w] for w in model(precheck_sent)[1]])
    print(oneline)