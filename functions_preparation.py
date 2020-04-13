# -*- coding:utf-8 -*-
from os import sep, system
from os.path import exists, isdir
from re import search
from time import sleep, strftime, localtime, time
from tkinter import filedialog, Tk, TclError
from shutil import copyfile
import sys


# 每一部jav的“结构体”
class JavFile(object):
    def __init__(self):
        self.file = 'ABC-123.mp4'  # 原文件名
        self.num = 'ABC-123'  # 车牌
        self.search = 'ABC%20123'  # 用于搜索javbus的车牌，javbus处理不了“-”“_”，算上“空格”，在url中把这三个换成了“%20”
        self.episodes = 1     # 第几集
        self.subt = ''        # 字幕文件名  ABC-123.srt


# 功能：获取用户选取的文件夹路径
# 参数：无
# 返回：路径str
# 辅助：tkinter.Tk，tkinter.filedialog，os.sep
def choose_directory():
    try:
        directory_root = Tk()
        directory_root.withdraw()
        path_work = filedialog.askdirectory()
        if path_work == '':
            print('你没有选择目录! 请重新选：')
            sleep(2)
            return choose_directory()
        else:
            # askdirectory 获得是 正斜杠 路径C:/，所以下面要把 / 换成 反斜杠\
            return path_work.replace('/', sep)
    except TclError:
        try:
            path_work = input("Please enter the path of your directory: ")
        except KeyboardInterrupt:
            sys.exit('Keyboard Interrupt detected. Exit now')

        if not exists(path_work) or not isdir(path_work):
            print('\"{0}\" does not exist or is not a valid directory. Try again.'.format(path_work))
            sleep(2)
            return choose_directory()
        return path_work
    except:
        raise

# 功能：检查 归类根目录 的合法性
# 参数：用户自定义的归类根目录，用户选择整理的文件夹路径
# 返回：归类根目录路径
# 辅助：os.sep，os.system
def check_classify_root(custom_root, root_choose):
    # 用户使用默认的“所选文件夹”
    if custom_root == '所选文件夹':
        return root_choose + sep + '归类完成'
    # 归类根目录 是 用户输入的路径c:\a，继续核实合法性
    else:
        custom_root = custom_root.rstrip(sep)
        # 用户输入的路径 不是 所选文件夹root_choose
        if custom_root != root_choose:
            if custom_root[:2] != root_choose[:2]:
                print('归类的根目录“', custom_root, '”和所选文件夹不在同一磁盘无法归类！请修正！')
                system('pause')
            if not exists(custom_root):
                print('归类的根目录“', custom_root, '”不存在！无法归类！请修正！')
                system('pause')
            return custom_root
        # 用户输入的路径 就是 所选文件夹root_choose
        else:
            return root_choose + sep + '归类完成'


# 功能：（如果需要为kodi整理头像）检查“演员头像for kodi.ini”、“演员头像”文件夹是否存在
# 参数：无
# 返回：无
# 辅助：os.path.exists，os.system，shutil.copyfile
def check_actors():
    if not exists('演员头像'):
        print('\n“演员头像”文件夹丢失！请把它放进exe的文件夹中！\n')
        system('pause')
    if not exists('【缺失的演员头像统计For Kodi】.ini'):
        if exists('actors_for_kodi.ini'):
            copyfile('actors_for_kodi.ini', '【缺失的演员头像统计For Kodi】.ini')
            print('\n“【缺失的演员头像统计For Kodi】.ini”成功！')
        else:
            print('\n请打开“【ini】重新创建ini.exe”创建丢失的程序组件!')
            system('pause')


# 功能：判断当前文件夹是否含有nfo
# 参数：文件们
# 返回：True
# 辅助：无
def exist_nfo(list_files):
    for file in list_files[::-1]:
        if file.endswith('.nfo'):
            return True
    return False


# 功能：判断是否有除了“.actors”"extrafanrt”外的其他文件夹
# 参数：文件夹list
# 返回：True
# 辅助：无
def exist_extra_folders(lst_folders):
    for folder in lst_folders:
        if folder != '.actors' and folder != 'extrafanart':
            return True
    return False


# 功能：记录整理的文件夹、整理的时间
# 参数：错误信息
# 返回：无
# 辅助：os.strftime, os.localtime, os.time,
def record_start(root_choose):
    msg = '已选择文件夹：' + root_choose + '  ' + strftime('%Y-%m-%d %H:%M:%S', localtime(time())) + '\n'
    txt = open('【记得清理它】失败记录.txt', 'a', encoding="utf-8")
    txt.write(msg)
    txt.close()
    txt = open('【记得清理它】警告信息.txt', 'a', encoding="utf-8")
    txt.write(msg)
    txt.close()
    txt = open('【记得清理它】新旧文件名清单.txt', 'a', encoding="utf-8")
    txt.write(msg)
    txt.close()


# 功能：记录错误信息
# 参数：错误信息
# 返回：无
# 辅助：无
def record_fail(fail_msg):
    print(fail_msg, end='')
    txt = open('【记得清理它】失败记录.txt', 'a', encoding="utf-8")
    txt.write(fail_msg)
    txt.close()


# 功能：记录警告信息
# 参数：警告信息
# 返回：无
# 辅助：无
def record_warn(warn_msg):
    txt = open('【记得清理它】警告信息.txt', 'a', encoding="utf-8")
    txt.write(warn_msg)
    txt.close()


# 功能：记录旧文件名
# 参数：新文件名，旧文件名
# 返回：无
# 辅助：无
def record_video_old(name_new, name_old):
    txt = open('【记得清理它】新旧文件名清单.txt', 'a', encoding="utf-8")
    txt.write('<<<< ' + name_old + '\n')
    txt.write('>>>> ' + name_new + '\n')
    txt.close()

