import os
import subprocess
import time
from pathlib import Path
from random import choice
from string import digits
import asyncio
import shutil


# import scan_and_replace

def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    # os.system('ls -l')


def open_apk(name,flag):
    try:
        # time.sleep(3)
        prevdir = os.getcwd()
        path = prevdir + '/all_mal_apps/' + name + '-new.apk'
        isExist = os.path.exists(path)
        if not isExist and not name == 'app3589' and not name == 'app2481' and not name == 'app2470' and not name == 'app4428' and not name == 'app3943' and flag == True:
            subprocess.run(["apktool", "-f", "d", name + ".apk"])  # open
            cd("..")
            os.system("python3 scan_and_replace.py " + name)
            cd("TestMalwareApps")
            subprocess.run(["apktool", "b", name])  # close
            cd(name)
            cd("dist")
            password = rand_pass()
            # keyboard.press_and_release(password)
            # print(password)
            subprocess.run(
            ["keytool", "-dname", "CN=Mark Smith, OU=Java, O=Oracle, L=Cupertino, S=California, C=US", "-alias", "bob",
             "-genkey", "-v", "-keystore", "mykey.keystore", "-storepass", "123456"])  # preparing the keystore
            subprocess.run(
            ["jarsigner", "-signedjar", name + "-new.apk", "-keystore", "mykey.keystore", name + ".apk", "bob",
             "-storepass", "123456"])  # jarsigner
            prevdir = os.getcwd()
            original = prevdir + '/' + name + '-new.apk'
            cd("..")
            cd("..")
            prevdir = os.getcwd()
            target = prevdir + '/all_mal_apps/' + name + '-new.apk'
            shutil.copyfile(original, target)
    except OSError as e:
        print('cant open or close', name)
    # subprocess.run([])
    # subprocess.run([keyboard.press_and_release(password)])

def rand_pass():
    code = list()
    for i in range(6):
        code.append(choice(digits))
    return code


# name= sys.argv[1]
# type=sys.argv[1]
# if type=='o':
def run():
    flag= True
    cd("TestMalwareApps")
    prevdir = os.getcwd()
    path = prevdir + '/all_mal_apps'
    isExist = os.path.exists(path)
    if not isExist:
        os.mkdir('all_mal_apps')
    for filename in os.listdir(Path().cwd()):
        if filename.endswith(".apk"):
            filename = filename.split('.')[0]
            # time.sleep(3)
            open_apk(filename,flag)
            flag= False
        # close_apk(filename)


# elif type=='c':
# close_apk()
if __name__ == "__main__":
    run()

# print("Wrong Input")
