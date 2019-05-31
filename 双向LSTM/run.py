import torch
import gensim
from dataset import *
import time
from model_load import *
from model_train import *

# 由于时间和算力限制效果较弱
# 训练集在mode_train中可以修改
modelname=trainModel()
# 默认的测试集为"test_pos1.txt"，可以修改
myresult=load_run(modelname,"test_pos1.txt")
print(myresult)