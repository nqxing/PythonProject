#!/usr/bin/env python
# coding=utf-8
from moviepy.editor import VideoFileClip
import os
import sys
import argparse
import pathlib

def get_file_times(filename):
    u"""
    获取视频时长（s:秒）
    """
    clip = VideoFileClip(filename)
    return clip.duration

def video_process(filename):
    u"""
     剪辑的区间在6到视频的总时长-6.5
    """
    clip=VideoFileClip(filename).subclip(6,int(get_file_times(filename))-6.5)
    file_name=os.path.splitext(filename)[0] #获取文件名（不带后缀）
    clip.write_videofile(file_name+"_fuck.mp4") #将文件变成文件名+fuck格式

def check_dir(path):
    u"""
    用来判断是文件，还是文件夹的方法
    """
    my_path=pathlib.Path(path)
    ex = my_path.exists()
    if ex:
        is_dir = my_path.is_dir()
        is_file = my_path.is_file()
    else:
        is_dir=False
        is_file=False
    return ex,is_dir,is_file

def fuck_dir(filepath):
    u"""
                文件夹的处理方法
    """
    pathDir =  os.listdir(filepath)
    for allDir in pathDir:
        filepath = os.path.abspath(filepath)
        child = os.path.join('%s/%s' % (filepath, allDir))
        file_format=os.path.splitext(child)[1]
        if file_format == ".mp4":
            print(child)
            video_process(child)

def fuck_file(path):
    u"""
    文件的处理方法
    """
    print("fuck from file")
    filepath = os.path.abspath(path)
    file_format=os.path.splitext(filepath)[1]
    if file_format == ".mp4":
        video_process(path)
    pass

# parse=argparse.ArgumentParser(description="fuck ajj") #解析命令行参数
# parse.add_argument("-i","--input",type=str,help="video item")
# args = parse.parse_args()
# video_item=args.input
# ex,is_dir,is_file=check_dir(video_item)
# print(ex,is_dir,is_file)
# if not ex:
#     print("the file is not exist!!!!!!\nPlease reinput")
# else:
#     if is_dir:
#        fuck_dir(video_item)
#     elif is_file:
#         fuck_file(video_item)
video_item = 'D:\\framework_demo\\1.mp4'
fuck_file(video_item)