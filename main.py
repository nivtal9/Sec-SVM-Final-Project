import os 
import sys
import subprocess
from contextlib import contextmanager

def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    os.system('ls -l')
    
def open_apk():
	subprocess.run(["apktool", "-f", "d", name+".apk"]) #open
	
def close_apk():
	subprocess.run(["apktool", "b", name])  #close
	cd(name)
	subprocess.run(["ls"])  #close
	cd("dist")
	subprocess.run(["keytool", "-alias","bob","-genkey","-v","-keystore", "mykey.keystore"])  #preparing the keystore
	subprocess.run(["jarsigner", "-signedjar",name+"2.apk","-keystore","mykey.keystore",name+".apk", "bob"]) #jarsigner
	
	 
name= sys.argv[1]
type=sys.argv[2]
if type=='o':
	open_apk()
elif type=='c':
	close_apk()
else:
	print("Wrong Input")
	
	"""
		apktool b magicDate
		cd magicDate
		cd dist
		keytool -alias bob -genkey -v -keystore mykey.keystore 
		jarsigner -signedjar new.apk -keystore mykey.keystore magicDate.apk bob
	"""
