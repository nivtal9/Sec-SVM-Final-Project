
from pathlib import Path

"""a function to find big registers files and their rows"""
def scan_Registers():
    b = False
    files = Path().cwd().glob("**/*.smali")
    for curr in files:
        with open(curr, 'r+') as f:
            count = 1
            for line in f:
                if "const-string v" in line:
                    str_v = int(line[line.find('g ') + 3:line.find(',')])
                    if str_v > 15:
                        b = True
                        print(curr)
                        print(count)
                count += 1
    if not b:
        print("no string registers above 16")


scan_Registers()
# and locals_num!=14 and locals_num!=31 and locals_num!=63
