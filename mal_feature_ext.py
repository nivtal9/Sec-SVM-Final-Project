import os
from pathlib import Path
import shutil
import glob
from shutil import rmtree
import time
import json

feature_array=[]
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    # os.system('ls -l')


cd("tool")
curr = os.getcwd()
mydir= os.getcwd()+'/app'
#try:
#    shutil.rmtree(mydir)
#except OSError as e:
#    print("Error: %s - %s." % (e.filename, e.strerror))

path = curr + '/app'
path2 = path + '/secsvm'
isExist = os.path.exists(path)
isExist2 = os.path.exists(path2)
if not isExist:
    os.mkdir('app')
cd('app')
if not isExist2:
    os.mkdir('secsvm')
prevdir = os.getcwd()
#cd('..')
#cd('..')
#cd('TestMalwareApps')
#cd('all_mal_apps')
#for file in os.listdir(os.getcwd()):
    #print(file)
#    original = os.getcwd() + '/' + file
#    target = prevdir + '/' + file.split('-', 1)[0] + '.apk'
    #print(original)
    #print(target)
#    shutil.copyfile(original, target)

cd('..')
cd('..')
"""
cd('TestMalwareApps')
curr = os.getcwd()
try:
    shutil.rmtree(curr)
except OSError as e:
    print("Error: %s - %s." % (e.filename, e.strerror))

cd('..')
"""

cd('tool')
os.system("python3 feature_ext.py app")

cd("app")
cd("results")
#with open('mal_train_app.json', "r") as all_features:
#    features = json.load(all_features)
    #feature_array.append('[')
#    feature_array.append(features[:-1])
#with open('mal_train_app.json', "w") as all_features:
#    json.dump(feature_array, all_features)
