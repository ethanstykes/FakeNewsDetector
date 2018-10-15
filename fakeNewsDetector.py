import os
script_dir = os.path.dirname(__file__)
def probMat(fileName):
    model={'W0rd1':['W0rd2','W0rd3']}
    file_read=open(fileName,"r",encoding="utf-8")
    file_list=file_read.read().strip().split()
    text=''
    for k in range(len(file_list)-1):
        text+=file_list[k]+" ";
        if file_list[k] not in model.keys():
            model[file_list[k]]=[file_list[k+1]];
        else:
            model[file_list[k]].append(file_list[k+1])
    #print(model)
    probmat={('W0rd1','W0rd2'):0.5,('W0rd1','W0rd3'):0.5}
    for i in range(len(model.keys())):
        word1=list(model.keys())[i]
        lenofVals=len(list(model.values())[i])
        addedVals=[]
        for k in range(0,lenofVals):
                if model[list(model.keys())[i]][k] not in addedVals:
                    word2=model[list(model.keys())[i]][k]
                    probmat[((word1,word2))]=1/lenofVals
                    addedVals.append(word2)
                elif model[list(model.keys())[i]][k] in addedVals:
                    word2=model[list(model.keys())[i]][k]
                    probmat[((word1,word2))]+=1/lenofVals
    return probmat 
probmatFake=probMat(os.path.join(script_dir, "server/fakeNews.txt"))
probmatReal=probMat(os.path.join(script_dir, "server/realNews.txt"))
#print(probmatReal)
probmatlimit=0
def detectFake(key,probmatlimit):
    fileName=os.path.join(script_dir, "testNews.txt")
    if key==0:
        probmat=probmatFake
    elif key==1:
        probmat=probmatReal
    FRfactor=1
    file_read=open(fileName,"r",encoding="utf-8")
    file_list=file_read.read().strip().split()
    for i in range(len(file_list)-1):
         probmatKeys=list(probmat.keys())
         for j in range(len(probmatKeys)):
             if (key==0 or probmatlimit>0) and file_list[i] == probmatKeys[j][0] and file_list[i+1] == probmatKeys[j][1]:
                 FRfactor+=probmat[(file_list[i],file_list[i+1])]
                 if key==0:
                     probmatlimit+=1
                 else:
                     probmatlimit-=1
    return FRfactor,probmatlimit
Ffactor,probmatlimit=detectFake(0,probmatlimit)
Rfactor,probmatlimit=detectFake(1,probmatlimit)
print("F:",Ffactor)
print("R:",Rfactor)
if Ffactor-1>Rfactor:
    print("This news is more likely fake")
elif Ffactor+1<Rfactor:
    print("This news is probably real")
else:
    print("Cannot determine")


