# encoding= utf-8
def cmpline(myline,theline):
    # 可能存在的问题——我们的标注为BEBE参考标注为BMME则不会被识别
    # fix the bug above
    wordlist=["S","B"]
    inoneword=False
    predwordnum=0
    reswordnum=0
    crtnum=0
    thenum=len(myline)
    for pos in range(thenum):
        mine=myline[pos]
        stnd=theline[pos]
        if mine in wordlist:
            predwordnum=predwordnum+1
        if stnd in wordlist:
            reswordnum=reswordnum+1
            if mine==stnd:
                if stnd=="B":
                    inoneword=True
                crtnum=crtnum+1
                continue
        if (stnd=='E' or mine=='E')and inoneword and stnd!=mine:
            crtnum=crtnum-1
            inoneword=False
    return crtnum,predwordnum,reswordnum

def cmpletter(myline,theline):
    thenum=len(myline)
    wordlist=["S","B"]
    crtnum=0
    for pos in range(thenum):
        mine=myline[pos]
        stnd=theline[pos]
        if mine==stnd:
            crtnum=crtnum+1
    return crtnum,thenum,thenum
#predres=open("thepredict.txt","r",encoding="utf-8")
#res=open("thepred.txt","r",encoding="utf-8")
# thelist=['B', 'E', 'S', 'B', 'E', 'S', 'B', 'E', 'S', 'B', 'E', 'B', 'E', 'S', 'B', 'E', 'S', 'B', 'E', 'S', 'B', 'E', 'S', 'B', 'E', 'B', 'E', 'S', 'B', 'E', 'S', 'S', 'B', 'E', 'S', 'B', 'E', 'S', 'S', 'B', 'E', 'B', 'E', 'B', 'E', 'S', 'S', 'B', 'E', 'B', 'E', 'B', 'E', 'S', 'S', 'B', 'E', 'B', 'E', 'B', 'E', 'S', 'B', 'E', 'S', 'S', 'B', 'E', 'S', 'B', 'E', 'S', 'B', 'E', 'B', 'E', 'S',
# 'B', 'E', 'S']
# hislist=['B', 'E', 'B', 'M', 'E', 'S', 'B', 'M', 'E', 'B', 'E', 'B', 'E', 'S', 'B', 'M', 'E', 'B', 'E', 'S', 'B', 'E', 'S', 'B', 'E', 'B', 'E', 'S', 'S', 'S', 'S', 'S', 'B', 'E', 'S', 'B', 'E', 'S', 'S', 'B', 'E', 'B', 'E', 'B', 'E', 'S', 'S', 'B', 'E', 'B', 'E', 'B', 'E', 'S', 'S', 'B', 'E', 'B', 'E', 'B', 'E', 'S', 'B', 'E', 'S', 'S', 'B', 'E', 'S', 'B', 'E', 'S', 'B', 'E', 'B', 'E', 'S',
# 'B', 'E', 'S']
# print(cmpline(thelist,hislist))