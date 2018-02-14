#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re

KeyWord = str()
TargetWord = str()
TargetPath = str()

def GetTarget():
    global KeyWord
    global TargetPath
    TargetPath = input("Please Enter the Disk Mark:")
    KeyWorld = input("Please Enter the Key word:")
    TargetWord  = input("Please Enter the Target word:")
    TargetPath += ':\\'
    return;

def EnterPathAndDoSth(Path):
    print('当前路径:' + Path)
    PathList = os.listdir(Path)
    if not PathList:
        return 0

    for i in PathList:
        TmpFileName = os.path.join(Path,i)
        print('当前文件(夹)' + TmpFileName)
        if os.path.isfile(TmpFileName):
            if CheckFileExtensionFilename(TmpFileName):
                File = open(TmpFileName,'r+',encoding = 'utf-8')
                string = File.read()
                string = string.replace(KeyWord,TargetWord)
                File.seek(0)
                File.write(string)
                File.close()
            else:
                return 0
        else:
            try:
                print('下一个路径:' + os.path.join(Path,i))
                EnterPathAndDoSth(os.path.join(Path,i))
            except FileNotFoundError:
                continue

def CheckFileExtensionFilename(Name):
    #You can revise this piece of code to Search other kinds file.
    if re.findall(r'(\S+.txt)',Name):
        return True
    else:
        return False

if __name__ == '__main__':
    GetTarget()
    EnterPathAndDoSth(TargetPath)
