import numpy as np 
from preprocess_pos import *

def load_file(filename):
    # 从文本中读取数据
    f=open(filename,"r",encoding="utf-8")
    lines=f.readlines()
    linelist=[]
    for line in lines:
        line=line.strip()
        linelist.append(line)
    return linelist

class HMM:
    def __init__(self):
        """
        初始化 HMM词性标注算法
        :return:
        """
        self.cixin_list = load_file('tag_set.txt')
        self.cixin_map = dict(zip(self.cixin_list, range(len(self.cixin_list))))  # 词性映射哈希表
        self.trans_pro_matrix = np.loadtxt('trans.txt') # 转移概率矩阵
        vocab_list = load_file('word_set.txt')
        self.delete=0
        self.vocab_map = dict(zip(vocab_list, range(len(vocab_list))))  # 词语映射哈希表
        self.emitter_pro_matrix = np.loadtxt('fasheMa.txt')  # 发射概率矩阵
        del vocab_list
        print("初始化完毕")

    def findNextTag(self ,pretag):
        for prenum in range(len(self.cixin_list)):
            if self.cixin_list[prenum]==pretag:
                break
        maxnum=0
        for nownum in range(len(self.cixin_list)):
            if self.trans_pro_matrix[nownum][prenum]>self.trans_pro_matrix[maxnum][prenum]:
                maxnum=nownum
        return maxnum

    def hmm(self, sentence_list):
        """
        :param sentence_list: 已分好词的句子列表
        :return: 对应每个词的词性列表
        """
        sentence_list = list(sentence_list)
        sentence_len = len(sentence_list)  # 句子长度
        cixin_len = len(self.cixin_list)  # 词性个数
        # 概率分布表 .[i, j, 0]表示第i个词为第j个词性的最优概率;.[i, j, 1]表示该最优概率的前一个词的词性索引,若为-1表示该词为第一个词无前词
        pro_table = np.zeros((sentence_len, cixin_len, 2))
        try:
            pro_table[0, :, 0] = self.emitter_pro_matrix[self.vocab_map[sentence_list[0]]]
            pro_table[0, :, 1] = -1
            for i in range(sentence_len)[1:]:
                # syTag=True
                for j in range(cixin_len):
                    # 这个是用来判断概率的
                    # if not self.vocab_map.get(sentence_list[i]):
                    #     syTag=False
                    #     sy=self.findNextTag(self.vocab_map[sentence_list[i]])
                    #     break
                    if self.emitter_pro_matrix[self.vocab_map[sentence_list[i]], j] == 0:
                        continue
                    pre_cixin_pro = pro_table[i-1, :, 0]
                    pre_cixin_pro *= self.trans_pro_matrix[j]
                    pre_cixin_pro *= self.emitter_pro_matrix[self.vocab_map[sentence_list[i]], j]
                    pro_table[i, j, 0] = np.max(pre_cixin_pro)
                    pro_table[i, j, 1] = np.where(pre_cixin_pro == np.max(pre_cixin_pro))[0][0]
            result_cixin_map = []
            sy = int(np.where(pro_table[-1, :, 0] == np.max(pro_table[-1, :, 0]))[0][0])
            t = -1
        except KeyError:
            # print(syTag)
            # self.delete=self.delete+1
            # print(self.delete)
            return
        while sy != -1:
            result_cixin_map.append(sy)
            sy = int(pro_table[t, sy, 1])
            t -= 1
        result_cixin = []

        for s in result_cixin_map[::-1]:
            result_cixin.append(self.cixin_list[s])
        return result_cixin

def score(histags,mytags):
    if mytags==None:
        return 0,0
    corrtnum=0
    for thesen in range(len(histags)):
        if histags[thesen]==mytags[thesen]:
            corrtnum=corrtnum+1
    return corrtnum,len(histags)

trainfile="train_pos.txt"
train_data,tag_set,word_set=loading_data(trainfile)
makeMartix(tag_set,train_data,word_set)
H_model=HMM()
testfile="test_pos1.txt"
resulttag=[]
corretNum=0
wordNum=0
test_data,test_tags,_=loading_data(testfile)
for testsen in test_data:
    tmplist=H_model.hmm(testsen[0])
    tmpnum1,tmpnum2=score(testsen[1],tmplist)
    corretNum=corretNum+tmpnum1
    wordNum=wordNum+tmpnum2
    resulttag.append(tmplist)
print(corretNum/wordNum)