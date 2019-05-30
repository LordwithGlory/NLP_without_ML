import re

# for the matched
def rpspace(matched):
    value=str(matched.group('value'))
    return value.replace(" ","")

f=open("devset/val_cws.txt","r",encoding="utf-8")
lines=f.readlines()
# the matched is begin with digital or < and finish with > or % or digital
# replace the space in the sentence
thestr=u"的解放军都是"
wlen=len(thestr)
for pos in range(wlen):
        print(thestr[pos])
p=re.compile(r'(?P<value>[0-9<]+[0-9|sub|sup|<|>|//|/./ ]+[0-9>%])')
for line in lines:
    output=re.sub(p,rpspace,line)
 #   if len(output)!=0:
#      print(output)