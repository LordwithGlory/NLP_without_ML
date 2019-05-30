import torch
from torch.autograd import Variable
import torch.nn.functional as F

class tnet(nn.Moudle):
    def _init_(self):
        super(tnet,self)._init_
        # Conv2d(in_c, out_c, filter_size, stride, padding) 二维神经卷积层
        self.conv1=nn.Conv2d(1,6,5)
        self.conv2=nn.Conv2d(6,16,5)
        # Linear(in_dim, out_dim, bias=True) 提供线性变换
        self.fc1=nn.Linear(16*5*5,120)
        self.fc2=nn.Linear(120,84)
        self.fc3=nn.Linear(84,10)

    def forward(self,x):
        # 二维最大池化层
        # 设置relu激活层
        x=F.max_pool1d(F.relu(self.conv1(x)),(2,2))
        # view(*shape), return the shared memory of objects
        x=x.view(-1,self.num_flat_features(x))

a={'a':1,'b':2}
b={'a':2,'c':3}
d={}
d.update(a)
d.update(b)
# get is better than [] and none is false
if d.get('d'):
    print(d.get('d'))
print(d)