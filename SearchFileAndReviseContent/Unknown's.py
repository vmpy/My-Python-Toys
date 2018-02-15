#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re   #正则表达式库.

#遍历盘符查找文件...
KeyWord = str()     #查找的关键字.
TargetWord = str()  #替换的字符串
TargetPath = str()  #目标盘符.

def GetTarget():
    """
    获取一些用户目标:
    Args:None.
    Returns:None
    """
    #全局变量声明.
    global KeyWord
    global TargetPath
    TargetPath = input("Please Enter the Disk Mark:")
    KeyWorld = input("Please Enter the Key word:")
    TargetWord  = input("Please Enter the Target word:")
    TargetPath += ':\\'     #盘符后加上这样标志才是正确的路径
    return;

def EnterPathAndDoSth(Path):
    print('当前路径:' + Path)
    PathList = os.listdir(Path)     #os.listdir(Path)返回一个关于该Path下的所有文件和文件夹的list.
    if not PathList:
        return 0
    #依次对Path下的文件和文件夹处理.
    for i in PathList:
        TmpFileName = os.path.join(Path,i)      #os.path.join连接两个字符串，使其成为一个合法的路径.
        print('当前文件(夹)' + TmpFileName)
        if os.path.isfile(TmpFileName):     #判断正在处理的路径是否为文件.
            if CheckFileExtensionFilename(TmpFileName):     #判断该文件的后缀名是不是我们想要的查找的文件，如果是，继续，或者继续循环.
                File = open(TmpFileName,'rb')   #打开文件，文本读写模式，utf-8解码.
                string = File.read().decode('utf-8','ignore')    #读取文件.
                if KeyWord in string:
                    string = string.replace(KeyWord,TargetWord)     #替换文件内容字符串.
                    File.close()
                    
                    File = open(TmpFileName,'wb')
                    File.write(string.encode('utf-8'))      #写入字符串.
                    File.close()
                else:
                    File.close()
                    continue
            else:
                continue
        else:
            try:
                print('下一个路径:' + os.path.join(Path,i))
                EnterPathAndDoSth(os.path.join(Path,i))     #如果是个路径，继续递归调用。os.path.join()函数作用同上.
            except FileNotFoundError:   #如果找不到文件（夹）,继续循环.
                continue

def CheckFileExtensionFilename(Name):
    """
    正则表达式查找后缀，如果是.txt返回True.反之,返回False.
    Args:Name:文件名（合法的绝对路径）
    Returns:
        见函数描述.
    """
    #You can revise this piece of code to Search other kinds file.
    if re.findall(r'(\S+.txt)',Name):
        return True
    else:
        return False

if __name__ == '__main__':  #调用代码.
    GetTarget()
    EnterPathAndDoSth(TargetPath)
