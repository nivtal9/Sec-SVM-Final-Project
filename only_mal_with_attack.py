import os
import shutil
import json

# import sys

# import scan_and_replace

labels_file = []
output = []
old = []

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
    with open('X_test.json', "r") as only_mal, open('y_test.json', "r") as dataset:
        mal = json.load(only_mal)
        old_features = json.load(dataset)
                    
    with open('X_test.json', "r") as labels, open('y_test.json', "w") as dataset:
        i = 0
        for line in labels:
            for label in line:
                if label == ',':
                    counter = counter + 1
                if label == '0':
                    continue
                    #output.append(old_features[counter])
                    tmp = tmp +1
                if label == '1'and i < len(old):
                    output.append(old[i])
                    labels_file.append(mal[counter])
                    i = i + 1
                if label == '1' and i >= len(old):
                    output.append(old_features[counter])
                    labels_file.append(mal[counter])
                    i = i + 1
                    
        json.dump(output, dataset)
    with open('X_test.json', "w") as labels:       
        json.dump(labels_file, labels)
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
    
