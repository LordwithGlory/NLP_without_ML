import torch
import os
import torch.autograd as autograd
import torch.nn as nn
import torch.optim as optim
import torch.tensor
import time
from dataset import *
from model_train import *
from model_load import *

# 默认训练集和为'train_pos999.txt'
trainFile='train_pos999.txt'
# 默认模型名称是"cixingnlpmodle99.m"
modelFile=model_train(trainFile)
# 默认测试集为'train_pos6k.txt'
model_load_run='train_pos6k.txt'
model_load_run(modelName)
# 由于训练结果存在误差因此不放置评估