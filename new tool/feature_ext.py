import staticAnalyzer
import sys
import os
from glob import glob
path=sys.argv[1]
result=os.listdir(path)
with open(str(sys.argv[1])+"/secsvm/"+sys.argv[1]+".json","w") as r:
        r.write("[")
r.close()
last=len(result)-1
for i in result:
        ind=result.index(i)
        if not(i.endswith(".apk")):
                continue
        try:
                staticAnalyzer.run(path+"/"+i, str(sys.argv[1])+"/",ind,last,str(sys.argv[1]))
        except Exception as e:
                print(e)
                print("file "+str(ind)+" failed")
                continue

with open(str(sys.argv[1])+"/secsvm/"+sys.argv[1]+".json","a") as r:
        r.write("]")
r.close()
