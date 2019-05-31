def readFile(filenam):
    inputf=open(filenam,"r",encoding="utf-8")
    outputf=open("lastgeshi.txt","w",encoding="utf-8")
    lines=inputf.readlines()
    count=0
    for line in lines:
        thelist=line.split()
        if line=="" or line==None or len(thelist)==0:
            outputf.write("\n")
            count+=1
            continue
        outputf.write(thelist[0]+"/"+thelist[1]+" ")
    outputf.close()
    print(count)

def data_process(data_file):
    data_list = []
    sentence_list = []
    count=0
    data_file = open(data_file, "r", encoding="utf-8")
    for line in data_file.readlines():
        if '<sub>' in line:
            count+=1
            continue
        elif '<sup>' in line:
            count+=1
            continue
        else:
            lineArr=line.strip().split()
            for i in range(len(lineArr)):
                if(lineArr[i]=='$$__' or lineArr[i]=='$$_'):
                    continue
                else:
                    word_tuple=tuple(lineArr[i].split('/'))
                    if len(word_tuple)!=2:
                        continue
                    else:
                        sentence_list.append(word_tuple)
                #print(sentence_list)
        data_list.append(sentence_list)
        sentence_list=[]
    print(count)
    return data_list

def corectFile(filename):
    inputf=open(filename,"r",encoding="utf-8")
    output=open("lastposinput.txt","w",encoding="utf-8")
    lines=inputf.readlines()
    for line in lines:
        if "<sub>" in line or "<sup>" in line:
            continue
        output.write(line)
    output.close()

readFile("predict.txt")
corectFile("test_posgeshi.txt")