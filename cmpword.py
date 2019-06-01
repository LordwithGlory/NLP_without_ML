def comLine(linea,lineb):
    # 默认lena小于lenb，即lena是我们的
    # 对于每行进行比较
    lenA=len(linea)
    lenB=len(lineb)
    if lenA==lenB:
        return True
    posa=0
    mylist=[]
    for i in range(lenB):
        if linea[posa:posa+1]==lineb[i:i+1]:
            posa+=1
            continue
        mylist.append(lineb[i:i+1])
    if not len(mylist)==1:
        print(mylist)
        print(linea)
        print(lineb)

def backtoOld(lineone):
    words=lineone.split()
    thesen=""
    for word in words:
        wlen=len(word)-1
        while word[wlen:wlen+1]!="/":
            wlen-=1
        thesen+=word[:wlen]
    f=open("backtoOld.txt","a",encoding="utf-8")
    f.write(thesen)
    f.write("\n")
    f.close()

f=open("test_pos2.txt","r",encoding="utf-8")
lines=f.readlines()
print(len(lines))
for line in lines:
    backtoOld(line)
f.close()
fa=open("backtoOld.txt","r",encoding="utf-8")
fb=open("test2.txt","r",encoding="utf-8")
linesa=fa.readlines()
linesb=fb.readlines()
if len(linesa)==len(linesb):
    for i in range(len(linesa)):
        comLine(linesa[i].strip().replace(" ",""),linesb[i])
    print("Equal")
print(len(linesa),len(linesb))