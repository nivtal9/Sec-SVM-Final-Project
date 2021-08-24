import json
from mainMenu import run
import os
import shutil
from zipfile import ZipFile
from pathlib import Path

labels = ['labels.json']
datasets = ['dataset.json']
apps = ['drebin_shas256.txt']
places_of_ones = []
names_of_mal = []

def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    # os.system('ls -l')

def fined_mal_in_test_labels():
    
    count = 0
    with open('X_test.json', "r") as files, open('y_test.json', "r") as dataset:
        data = json.load(dataset)
        print(len(data))
        # counter=0 #checks the number of 1's labeled.
        # counteriho=0 #checks the number of generated keys found in text file.
        for line in files:
            for character in line:
                # print(character)
                if character == ',':
                    count = count + 1
                if character == '1':
                    # counter = counter + 1
                    places_of_ones.append(count)  # what is this for?
                    #print(count)
                    wordcheck = data[count]["sha256"]
                    with open('drebin_shas256.txt', 'r') as f:
                        for lines in f:
                            key, val = lines.strip().split(',')
                            if wordcheck == val:
                                # counteriho = counteriho + 1
                                names_of_mal.append(key)
                    # print(counter)
                    # print(data[count]["sha256"])
        files.close()
        #with ZipFile('drebin_apps.zip', 'r') as zipObj:
        """for app in names_of_mal:
                print("Extracting " + app + ", please wait..")
                zipObj.extract(app, path='TestMalwareApps', pwd=b'Cyberadmin26')"""

        path = os.getcwd() + '/TestMalwareApps'
        path2 = os.getcwd() + '/TestMalwareApps/all_mal_apps'
        isExist = os.path.exists(path)
        if not isExist:
            os.mkdir(path)
            os.mkdir(path2)

        #for app in names_of_mal:
            #original = os.getcwd() + '/drebin_apps/' + app
            #target = os.getcwd() + '/TestMalwareApps/' + app
            #shutil.copyfile(original, target)
        cd("tool")
        curr = os.getcwd()
        mydir= os.getcwd()+'/app'
        try:
            shutil.rmtree(mydir)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
        path = curr + '/app'
        isExist = os.path.exists(path)
        if not isExist:
            os.mkdir('app')
        cd("..")
        for app in names_of_mal:
            try:
                original = os.getcwd() + '/drebin_apps/all_mal_apps/' + app.split('.')[0] + '-new.apk'
                #target = os.getcwd() + '/TestMalwareApps/all_mal_apps/' + app.split('.')[0] + '-new.apk'
                target = os.getcwd() + '/tool/app/' + app
                shutil.copyfile(original, target)

            except OSError as e:
                print("app not found")
                

        # print(counter)
        # print(counteriho)




"""
#  [{"sha256": "30C21815C56540BC766DEA93772B2F20CE7C745F9281B2378944D70B2ECEE137", 
def fined_mal_in_test_datasets():
    count = 0;
    name=""
    file = open('y_test.json', "r")
    for line in file:
        for character in line:
            #print(character)
            if(character == '{'):
                count=count+1
            if(count in places_of_ones):
                print(count)
                for char in line:
                    if(char == ' '):
                        name=""
                        for char in line:
                            if(char=='"' and name != "" ):
                                name=name+char
                                break
                            name=name+char
                        names_of_mal.append(name)
                        break
    file.close()
    
"""

fined_mal_in_test_labels()
run()
cd("..")
# print(places_of_ones)
# fined_mal_in_test_datasets()


# print(names_of_mal)
