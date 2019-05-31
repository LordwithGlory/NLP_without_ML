import numpy as np
import datetime
from dataset import *
from model import *
from evaluate import *

# 对训练集训练
train_hmm('train_pos.txt')
# 对预测集预测
predict_hmm('fencires.txt')
# 预测结果写入
readFile("predict.txt")
# 预测集合重写
corectFile("predict.txt")
# 输出预测结果
envaluate()