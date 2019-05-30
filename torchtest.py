import torch
from torch.autograd import Variable

# x 包含一个2x2张量和一个requires_grad参数
x=Variable(torch.ones(2,2),requires_grad=True)
# y 包含一个2x2张量是在x上整体加2，以及一个grad_fn参数
y=x+2
z=y*y+3
# out的grad_fn居然和z的不一样震惊咧
out=z.mean()
out.backward()
# before the backward(), the grad is none and we can calutate the grad by format
# print(x.grad)
x=torch.randn(3)
x=Variable(x,requires_grad=True)
y=x*2
# 标准差小于1000的时候
while y.data.norm()<1000:
    y=y*2
gradients=torch.FloatTensor([1,0.1,0.00001])
y.backward(gradients)
print(x.grad)