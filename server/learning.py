import os
script_dir = os.path.dirname(__file__)
import pymysql
def probMat(fileName):
    model={'W0rd1':['W0rd2','W0rd3']}
    file_read=open(fileName,"r",encoding="utf-8")
    file_list=file_read.read().strip().replace("'", " ").replace("."," . ").split()
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
        for k in range(0,lenofVals):
            word2=model[list(model.keys())[i]][k]
            probmat[((word1,word2))]=0
        for k in range(0,lenofVals):
            word2=model[list(model.keys())[i]][k]
            probmat[((word1,word2))]+=1/lenofVals
    return probmat
probmatFake=probMat(os.path.join(script_dir, "fakeNews.txt"))
probmatReal=probMat(os.path.join(script_dir, "realNews.txt"))

db = pymysql.connect("localhost","user","password","mysql")
sql = "truncate table probmatreal"
db.cursor().execute(sql)
sql = "truncate table probmatfake"
db.cursor().execute(sql)
probmatKeys=list(probmatReal.keys())
probmatValues=list(probmatReal.values())
for i in range(len(probmatKeys)):
    sql = "insert into probmatreal values('"+probmatKeys[i][0]+"','"+probmatKeys[i][1]+"',"+str(probmatValues[i])+")"
    print("realmat.insert('"+probmatKeys[i][0]+"','"+probmatKeys[i][1]+"',"+str(probmatValues[i])+")")
    db.cursor().execute(sql)
    db.commit()
probmatKeys=list(probmatFake.keys())
probmatValues=list(probmatFake.values())
for i in range(len(probmatKeys)):
    sql = "insert into probmatfake values('"+probmatKeys[i][0]+"','"+probmatKeys[i][1]+"',"+str(probmatValues[i])+")"
    print("fakemat.insert('"+probmatKeys[i][0]+"','"+probmatKeys[i][1]+"',"+str(probmatValues[i])+")")
    db.cursor().execute(sql)
    db.commit()

