import os 
import sys
import subprocess
from pathlib import Path


def add_values_in_dict(sample_dict, key, list_of_values):
    """Append multiple values to a key in the given dictionary"""
    if key not in sample_dict:
        sample_dict[key] = list()
    sample_dict[key].extend(list_of_values)
    return sample_dict
def scan_locals():
	files = Path().cwd().glob("**/*.smali")
	print(Path())
	for curr in files:
		count=0
		locals_change_to = {}
		string_change_to = {}
		with open(curr,'r+') as f:
			for line in f:
				count+=1
				if '.method' in line:
					for line in f:
						count+=1
						if ".locals" in line:
							locals_num=int(line[12:])
							locals_line=count
						if "const-string" in line:
							if(len(line)-line.find('"')>4):
								str_v=line[line.find('g ')+2:line.find(',')] 		#holds v0/v1/v2...
								const_string_line=count 				#holds the const-string line
								string_to_cut=line[line.find('"')+1:len(line)-2] 	#holds the string to cut
								#print(string_to_cut)
								if(string_to_cut=='\\n' or string_to_cut=='\\t' or string_to_cut=='\\r'):
									#print("hello")
									continue
								firstpart= '"'+string_to_cut[:int(len(string_to_cut)/2)]+'"'
								secondpart='"'+string_to_cut[int(len(string_to_cut)/2):]+'"'
								new_v=str(locals_num+1)
								#print(string_to_cut)
								add_values_in_dict(locals_change_to,locals_line-1,["    .locals "+new_v])
								add_values_in_dict(string_change_to,const_string_line-1,[str_v,
							"    const-string "+str_v+", "+firstpart+"\n\n    const-string v"+new_v+", "+secondpart+"\n\n    invoke-virtual {"+str_v+", "+str_v+"}, Ljava/lang/String;->append(Ljava/lang/String;)Ljava/lang/String;\n\n    invoke-virtual {"+str_v+", v"+new_v+"}, Ljava/lang/String;->append(Ljava/lang/String;)Ljava/lang/String;\n\n    invoke-virtual {"+str_v+"}, Ljava/lang/String;->toString()Ljava/lang/String;\n\n    move-result-object "+str_v+""])							

						elif ".end method" in line:
							break
		if(locals_change_to):
			print(locals_change_to)
			print(curr)
			a_file = open(curr, "r")
			list_of_lines = a_file. readlines()
			for k,v in locals_change_to.items():
				list_of_lines[k]=v[0]+"\n"
			for k,v in string_change_to.items():
				list_of_lines[k]=v[1]+"\n"
			a_file. close()	
			a_file = open(curr, "w")
			a_file. writelines(list_of_lines)
			a_file. close()

scan_locals()

	
	
