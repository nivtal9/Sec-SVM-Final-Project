import os
import sys
import subprocess
from pathlib import Path
import re

# [0, 5, 10, 15]

locals_change_to = {}
string_change_to = {}

all_locals = []
used_locals = []
not_used_locals = []
can_use_locals = []
can_use_after_string = []


def add_values_in_dict(sample_dict, key, list_of_values):
    """Append multiple values to a key in the given dictionary"""
    if key not in sample_dict:
        sample_dict[key] = list()
    sample_dict[key].extend(list_of_values)
    return sample_dict


def character_indexes_comprehension(my_line, can_use):
    string = my_line
    match = ", v"
    match2 = " v"
    # temp= [index for index, character in enumerate(string) if character == match or character == match2 ]
    temp = [m.start() for m in re.finditer('{v', my_line)]
    temp1 = [m.start() for m in re.finditer(' v', my_line)]
    temp = temp + temp1
    if temp:
        for place in range(0, len(temp)):
            current_v = None
            try:
                current_v = int(my_line[temp[place] + 2: my_line.find(',', temp[place])])
            except ValueError:
                try:
                    current_v = int(my_line[temp[place] + 2: my_line.find(' ', temp[place])])
                except ValueError:
                    try:
                        current_v = int(my_line[temp[place] + 2: my_line.find('}', temp[place])])
                    except ValueError:
                        pass

            if current_v:
                used_locals.append(current_v) if (current_v) not in used_locals else used_locals

                if can_use == 1 and current_v in can_use_locals:
                    can_use_locals.remove(current_v)
                    return can_use_locals
                if can_use == 2 and current_v in can_use_after_string:
                    can_use_after_string.remove(current_v)
                    return can_use_after_string
            if can_use == 1:
                return can_use_locals
            else:
                return can_use_after_string

    return None


def read_after_string(line, remember_lines, can_use_after_string):
    while remember_lines[line] and ".end method" in remember_lines[line]:
        can_use_after_string = character_indexes_comprehension(remember_lines[line], 2)
        line += 1
    # print('can_use_after_string 00:' ,can_use_after_string)


def scan_locals():
    flag = False
    can_use_after_string = []
    can_use_locals = []
    os.chdir(os.getcwd() + "/TestMalwareApps/" + sys.argv[1])
    files = Path().cwd().glob("**/*.smali")
    print(files)
    for curr in files:
        # print (curr)
        # print('bl\na\nl\na\nl\na\nlala\n')
        count = 0
        locals_change_to = {}
        string_change_to = {}
        remember_file = open(curr, "r")
        remember_lines = remember_file.readlines()
        remember_file.close()
        with open(curr, 'r+') as f:
            dirpath = str(curr)
            parent_folder = dirpath.split(sep="/")
            parent_folder = str(parent_folder[len(parent_folder) - 2])
            # print(parent_folder)
            for line in f:
                count += 1
                if '.method' in line:
                    parameter_num = line[line.find('(') + 2:line.find(')')]
                    parameter_num = parameter_num.count(';') + 1
                    if '.method private' in line:
                        parameter_num += 1
                    if '.method public' in line:
                        parameter_num += 2
                    if '.method protected' in line:
                        parameter_num += 2
                        # continue
                    if 'constructor' in line or 'direct methods' in prev_line:
                        continue
                    # if 'Landroid/view/View;' in line or 'Ljava/lang/String' in line:
                    #	continue
                    flag = False
                    flag2 = False
                    prev_line = line
                    for line in f:
                        count += 1
                        if ".locals" in line:
                            locals_num = int(line[12:])
                            locals_line = count
                            if ((locals_num + parameter_num) >= 15):
                                can_use_locals = []
                                can_use_after_string = []
                                can_use_locals = [x for x in range(0, locals_num - parameter_num - 1)]
                                can_use_after_string = [x for x in range(0, locals_num - parameter_num - 1)]
                                flag = True
                            else:
                                can_use_locals = []
                                can_use_after_string = []
                                can_use_locals = [x for x in range(0, locals_num - parameter_num - 1)]
                                can_use_after_string = [x for x in range(0, locals_num - parameter_num - 1)]
                                flag = False
                                temp = None
                        if flag == True:
                            can_use_locals = character_indexes_comprehension(line, 1)
                        if 'Ljava/io/File' in line:
                            flag2 = True

                        if "const-string v" in line and flag2 == False:
                            read_after_string(count, remember_lines, can_use_after_string)
                            if can_use_after_string:
                                for c in can_use_after_string:
                                    if (can_use_locals):
                                        can_use_locals.append(c) if c not in can_use_locals else can_use_locals
                                    else:
                                        can_use_locals = []
                                        can_use_locals.append(c)
                            str_v = line[line.find('g ') + 2:line.find(',')]  # holds v0/v1/v2...
                            if can_use_locals and int(str_v[1:]) in can_use_locals:
                                can_use_locals.remove(int(str_v[1:]))
                            if (len(line) - line.find('"') > 6 and (flag == False or can_use_locals)):
                                # print(parent_folder)
                                # print(prev_line)
                                const_string_line = count  # holds the const-string line
                                string_to_cut = line[line.find('"') + 1:len(line) - 2]  # holds the string to cut
                                # print(string_to_cut)
                                # if 'com ' in line or 'com.' in line or 'android' in line or 'generic' in line:
                                #	continue
                                # if (parent_folder in string_to_cut or "/"+parent_folder+"/" in  prev_line):
                                #	continue
                                if (int(str_v[1:]) > (16 - parameter_num)):
                                    continue
                                if (string_to_cut == '\\n' or string_to_cut == '\\t' or string_to_cut == '\\r' or
                                        string_to_cut[0] == '['):
                                    continue
                                if can_use_after_string:
                                    continue
                                if ("\\\'t" in line):
                                    continue
                                if string_to_cut.lower().endswith(('.png', '.jpg', 'jpeg', 'zip', 'json', 'txt', 'mp3', 'mp4' )):
                                    continue
                                pattern1 = r"(0\\u.*)"
                                pattern2 = r"(\\.*\\){1}"
                                pattern3 = r"(([a-zA-Z0-9]+\.){2}([_a-zA-Z0-9]))"
                                pattern4 = r"(\\u.*)"
                                pattern5 = r"(\\.%.\\)"
                                pattern6 = r"('.+')"
                                if re.search(pattern1, line):
                                    # print('yes!')
                                    continue
                                elif re.search(pattern4, line):
                                    # print('yes!')
                                    continue
                                elif re.search(pattern5, line):
                                    # print('yes!')
                                    continue
                                elif re.search(pattern6, line):
                                    match = re.search(pattern6, line)
                                    firstpart = '"' + string_to_cut[:match.start()] + '"'
                                    secondpart = '"' + string_to_cut[match.start():] + '"'
                                    # print(match.end())


                                # if re.search(pattern2,line):
                                #	match=re.search(pattern2,line)
                                #	firstpart= '"'+string_to_cut[:match.start()]+'"'
                                #	secondpart='"'+string_to_cut[match.start():]+'"'
                                else:
                                    firstpart = '"' + string_to_cut[:int(len(string_to_cut) / 2)] + '"'
                                    secondpart = '"' + string_to_cut[int(len(string_to_cut) / 2):] + '"'
                                # if ( firstpart[len(firstpart)-2] == '\\' ):
                                #	print(firstpart[len(firstpart)-2])
                                #	continue
                                if secondpart.find('""') or firstpart.find('""'):
                                    continue
                                if flag == False:
                                    if can_use_locals:
                                        new_v = str(can_use_locals[0])
                                    else:
                                        new_v = str(locals_num)
                                    new_locals = str(locals_num + 1)
                                else:
                                    new_v = str(can_use_locals[0])
                                    new_locals = str(locals_num)
                                add_values_in_dict(locals_change_to, locals_line - 1, ["    .locals " + new_locals])
                                print()
                                print()
                                print(string_to_cut)
                                add_values_in_dict(string_change_to, const_string_line - 1, [str_v,
                                                                                             "    const-string " + str_v + ", " + firstpart + "\n\n    const-string v" + new_v + ", " + secondpart + "\n\n    invoke-virtual {" + str_v + ", v" + new_v + "}, Ljava/lang/String;->concat(Ljava/lang/String;)Ljava/lang/String;\n\n    move-result-object " + str_v + ""])
                            prev_line = line

                        elif ".end method" in line:
                            prev_line = line
                            break

                        if line != "\n":
                            prev_line = line
                    if line != "\n":
                        prev_line = line
                if line != "\n":
                    prev_line = line
        if (locals_change_to):
            # print(locals_change_to)
            # print(curr)
            a_file = open(curr, "r")
            list_of_lines = a_file.readlines()
            for k, v in locals_change_to.items():
                list_of_lines[k] = v[0] + "\n"
            for k, v in string_change_to.items():
                list_of_lines[k] = v[1] + "\n"
            a_file.close()
            a_file = open(curr, "w")
            a_file.writelines(list_of_lines)
            a_file.close()


scan_locals()
