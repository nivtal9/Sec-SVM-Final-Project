import os
#import sys
import subprocess
import time
#from contextlib import contextmanager
from pathlib import Path
import keyboard
from random import choice
from string import digits
import asyncio


# import scan_and_replace

def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    os.system('ls -l')


def open_apk(name):
    time.sleep(3)
    subprocess.run(["apktool", "-f", "d", name + ".apk"])  # open
    os.system("python3 scan_and_replace.py " + name)
    subprocess.run(["apktool", "b", name])  # close
    cd(name)
    cd("dist")
    #password = rand_pass()
    #keyboard.press_and_release(password)
    #print(password)
    subprocess.run(
        ["keytool", "-dname", "CN=Mark Smith, OU=Java, O=Oracle, L=Cupertino, S=California, C=US", "-alias", "bob", "-genkey", "-v", "-keystore", "mykey.keystore", "-storepass", "123456"])# preparing the keystore
    subprocess.run(["jarsigner", "-signedjar", name + "-new.apk", "-keystore", "mykey.keystore", name + ".apk",
                    "bob", "-storepass", "123456"])  # jarsigner
    #os.system('123456')
    cd("..")
    cd("..")
    #subprocess.run([])
    #subprocess.run([keyboard.press_and_release(password)])
    #keyboard.press_and_release(password)


def rand_pass():
    code = list()
    for i in range(6):
        code.append(choice(digits))
    return code


# name= sys.argv[1]
# type=sys.argv[1]
# if type=='o':
for filename in os.listdir(Path().cwd()):
    if filename.endswith(".apk"):
        filename = filename.split('.')[0]
        time.sleep(3)
        open_apk(filename)
        # close_apk(filename)
# elif type=='c':
# close_apk()
# else:
# print("Wrong Input")
