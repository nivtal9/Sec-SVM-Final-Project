# Sec-SVM: Final Project

[Overleaf Document](https://www.overleaf.com/read/fnqvkdtqjjnj)

# Sec-svm final Day presentation

## Introduction

Malware in application is a crucial part in malware detection, each person have a personal device and/or work devices which uses android OS.
Drebin is a tool for malware detection which analysis the application code and uses weights to divide the categories in the shape of malware patterns.
Sec-svm is an improvement to Drebin. This model give more efficient weights (even to benign categories!) to the divided categories where Drebin is excluding them from the final analyzation.

## Our goal

The goal of this project is to find breaches in Sec-svm algorithm by obfuscating the system and reviewing that Sec-svm won't recognize the application as malware. 
This Work is on an existing malware attack that Sec-svm detects as malware app. 
The method is to avoid detection by split several code lines inside an application and re-attach them so that Sec-svm won't recognize the malware lines.
Checking that the functionality of the application won't be harm by our attack. We used droid Bot to ensure that.
Fixing the feature analyzer in a way that Sec-svm model will detect (in a generic way) our attack of cutting and re-attaching the string lines.

## Starting point

After we finished Literature review on Malware detection, Drebin and Sec-svm, we tried to develop a code which convert from Drebin dataset to Sec-svm dataset to reduce processed running time but we recognized that Drebin won't refer to the same features as Sec-svm like we said in the introduction, so there was no improvement to run time. Also, this help us realize the difference between the models.
we’ve been introduced to Sec-svm feature extraction code and the families that the model reference to. This tool helps to get all the features rather benign or malware from several apps to a single json file that sec-svm can use as dataset.
Then we got Sec-svm code and train-test dataset that we can give Sec-svm to process and deliver the accuracy and recall score for detection.

## Work process

1. The first step of the work is getting the basic requirements to work with applications and application files. We needed to understand and install Emulator, apktool, jarsigner and smali syntax. 
Created a script that loops on each apk file in a given directory and executes the following steps:
  - Decodes the app with apktool command and in particularly – a smali folder of the application
  - Execute scan_and_replace.py script on each smali file and put our attack lines instead each string lines.
  - Build the application after the attack is inserted with apktool command
  - Signing the application with keytool and jarsigner commands for future functionality testing and analyzing.
2. Started planning the attack process, within the steps:
  * reverse engineering on java split and append code sample to smali so we can get the manipulation main string that we replace with normal smali string line. When we first started with append method, we observed that the application won't build and sign correctly because append used stringBuilder which causes problems, so we switch to concat which uses String and that resolve the problem.
Each method of the application that written in samli are having maximum number of registers to hold. When we tried to add +1 local register to a method that already had more then 16 local register we came across a problem that we exceed the maximum number so the next step was to overcome this with current registers that we can use just for cut proposes and without intervene the normal process of the method.
  * Also, some strings were problematic to change so we excludes them from the changing process. (‘/t’ ‘/r’ etc.)
3. Poster planning – for demonstration day at 8.6.21 we had to present a poster that summarize introduction, main goal and the process that we did so far. Poster is attached in Github.
4. we needed to enlarge the number of apps that we worked on within sec-svm and our attack. We got source of 4000+ malware applications that we can test out attack on. Also a sha256 text file that helps us with finding the application after feature extraction.
5. Developed a scheme that will help us get reliable and consistent results from sec-svm. The scheme is happening 5 times and saving the Sec-svm results each time:
- Running Sec-svm on the dataset and labels that we have in train/test and saving the results of the run
- We merge the dataset to one json and one label files and then splits them to 80% train and 20% test
- locating applications in new test folder as malware (if the label in that spot marked by 1) and organizes them into one directory.
- Executes our attack on the founded application folder from previous step
- Feature extraction from the manipulated application from previous step to one json file.
- Replacing from the 20% test dataset the malware features respectively with malware features from our newly created json file from previous step.
- Final step, we swap the 4 new files (train dataset and labels, test dataset and labels) with the existing 4 files in train/test.

## Scripts
- [scan_and_replace.py](https://github.com/nivtal9/Sec-SVM-Final-Project/blob/main/scan_and_replace.py) - Gets a directory and runs recursively on each smali file. The script working on each method scopes and searching for local registers he can use for splitting the string if the locals number is above 16.
if the method not exceeding the maximum locals number we just add +1 the locals and continue the string change.
After we checked that we can perform the string change from the perspective of locals numbers and specific exclude of string type (‘/t’, regax pattern of computer addresses, etc.) we cut the string to 2 and then “concat” it together again for obfuscation.
- [merge_and_split.py](https://github.com/nivtal9/Sec-SVM-Final-Project/blob/main/merge_and_split.py) - Gets dataset of test+labels and dataset of train+labels.
Performs a merge to one big dataset and matching labels, then shuffle and split (while maintain order) to 80% train and 20% test for future Sec-svm analyze.
- [find_mal.py](https://github.com/nivtal9/Sec-SVM-Final-Project/blob/main/find_mal.py) - This script going through the new test labels and picks the malware spots in the json (mark as 1), then going to the new test dataset and picks the sha256 (generated unique key of the app) key and gets from txt file which we got (drebin_shas256.txt) the actual app name. 
Then we organize all the founded apps in one directory and performs our attack on those application.
- [mainMenu.py](https://github.com/nivtal9/Sec-SVM-Final-Project/blob/main/mainMenu.py) - This script are called from fined.py and loops on each application that we found in the previous script and Executes the following: decodes the app, execute scan_and_replace.py and finally - build and sign the application afterwards.
- [mal_feature_ext.py](https://github.com/nivtal9/Sec-SVM-Final-Project/blob/main/mal_feature_ext.py) - This script gets all the manipulated founded apps that we found in fined.py and performs feature extraction.
The output is one json that contains the features of those post-attack apps.
- [replace_mal.py](https://github.com/nivtal9/Sec-SVM-Final-Project/blob/main/replace_mal.py) - This script uses the new json file that we got from previous script and then scanning the new test label places of 1’s and replaces respectively a feature from our new json instead a malware feature in the new test dataset. After all the replacement we want to run Sec-svm again on the new created dataset, so we replace the train and test old json’s with the newly created json’s.






