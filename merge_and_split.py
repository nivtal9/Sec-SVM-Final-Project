import json
import os

from sklearn.model_selection import train_test_split

label_files = ['train/labels.json', 'test/labels.json']
dataset_files = ['train/train_dataset.json', 'test/test_dataset.json']


def merge_JsonFiles(filename, new_name):
    prevdir = os.getcwd()
    path = prevdir + '/' + new_name
    isExist = os.path.exists(path)
    if isExist:
        os.remove(new_name)
    result = list()
    for f1 in filename:
        with open(f1, 'r') as infile:
            result.extend(json.load(infile))

    with open(new_name, 'w') as output_file:
        json.dump(result, output_file)
    #print(result)


merge_JsonFiles(label_files, 'labels.json')
merge_JsonFiles(dataset_files, 'dataset.json')


with open('labels.json', 'r') as labels, open('dataset.json', 'r') as dataset:
    #arr = json.load(labels)
    #print(arr)
    X_train, X_test, y_train, y_test = train_test_split(json.load(labels), json.load(dataset), test_size=0.2, train_size=0.8 , shuffle=True)
    #X_train, X_test, y_train, y_test = train_test_split(labels, dataset
     #                                                   , test_size=0.2, train_size=0.8, random_state=0, shuffle=False)

with open('X_train.json', 'w') as output_file:
    json.dump(X_train, output_file)
with open('X_test.json', 'w') as output_file:    
    json.dump(X_test, output_file)
with open('y_train.json', 'w') as output_file:    
    json.dump(y_train, output_file)
with open('y_test.json', 'w') as output_file:    
    json.dump(y_test, output_file)
