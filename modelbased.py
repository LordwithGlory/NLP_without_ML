import torch
import os
from dataset import *
from train_FENCI_END import BiLSTM_CRF
import torch.autograd as autograd
import torch.nn as nn
import torch.optim as optim
import torch.tensor

training_data=annyfile("train_cws.txt")
word_to_ix = {}
for sentence, tags in training_data:
    for word in sentence:
        if word not in word_to_ix:
            word_to_ix[word] = len(word_to_ix)
print("in line 16")
model=torch.load_state_dict(torch.load("fencinlpmodle99.m"))
print("in line 19")
model.eval()
test_data=annyfile("test_cws1.txt")
print("in line 22")
with torch.no_grad():
    print("IN TESTING")
    for i in range(len(test_data)):
        precheck_sent = prepare_sequence(test_data[i][0], word_to_ix)
        print(model(precheck_sent))