import os
import shutil
import json

# import sys

# import scan_and_replace

old = []
output = []

def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))


def take_features_output():
    cd("tool")
    cd("app")
    cd("results")
    prevdir = os.getcwd()
    original = prevdir + '/' + 'mal_train_app.json'
    cd("..")
    cd("..")
    cd("..")
    prevdir = os.getcwd()
    target = prevdir + '/' + 'mal_train_app.json'
    shutil.copyfile(original, target)


def replacement():
    count = 0
    # sys.stdout = open("test.txt", "w")
    with open('mal_train_app.json', "r") as features, open('y_test.json', "r") as dataset:
        new_features = json.load(features)
        old_features = json.load(dataset)
    with open('mal_train_app.json', "r") as features:
        for new_line in features:
            for new_character in new_line:
                if new_character == '{':
                    # print(new_features[count]["sha256"])
                    feature_check = new_features[count]
                    old.append(feature_check)
                    # print(feature_check)
                    count = count + 1

    counter = 0
    tmp = 0
    #print(len(old_features))  # =1
    with open('X_test.json', "r") as labels, open('y_test.json', "w") as dataset:
        i = 0
        # print(len(old_features)) #=1
        # print(len(old)) #=895
        for line in labels:
            for label in line:
                # print("counter: " ,counter)
                # print("i: " ,i)
                # print(character)
                if label == ',':
                    counter = counter + 1
                if label == '0':
                    # print(counter)
                    output.append(old_features[counter])
                    tmp = tmp +1
                    #json.dump(old_features[counter], dataset, separators=(',', ':'))
                    #json.dump(chr(44)+chr(32), dataset)
                    # i = i + 1
                if label == '1' and i < len(old):
                    output.append(old[i])
                    i = i + 1
                    tmp = tmp +1
                    #json.dump(old[i], dataset, separators=(',', ':'))
                if label == '1' and i >= len(old): 
                    output.append(old_features[counter])                  
                    i = i + 1
                    tmp = tmp +1
        #json.dump(chr(93), dataset)
        print(len(old_features))
        print(counter)
        print(tmp)
        json.dump(output, dataset)
        # old_features[counter]=feature_check
    original = os.getcwd() + "/y_test.json"
    target = os.getcwd() + "/test/test_dataset.json"
    shutil.copyfile(original, target)
    original = os.getcwd() + "/X_test.json"
    target = os.getcwd() + "/test/labels.json"
    shutil.copyfile(original, target)
    original = os.getcwd() + "/y_train.json"
    target = os.getcwd() + "/train/train_dataset.json"
    shutil.copyfile(original, target)
    original = os.getcwd() + "/X_train.json"
    target = os.getcwd() + "/train/labels.json"
    shutil.copyfile(original, target)



if __name__ == "__main__":
    take_features_output()
    replacement()
    
