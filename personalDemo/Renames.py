import os, os.path, time

def update_file_houz():
    files = os.listdir("D:\\xj")#列出当前目录下所有的文件
    for filename in files:
        portion = os.path.splitext(filename)#分离文件名字和后缀
        print(portion)
        if portion[1] ==".mp3":#根据后缀来修改,如无后缀则空
            newname = portion[0]+".jpg"#要改的新后缀
            ##newname = portion[1]+".mp3"#要改的新后缀
            os.chdir("D:\\xj")#切换文件路径,如无路径则要新建或者路径同上,做好备份
            os.rename(filename,newname)

def update_file_name(file):
    ''' file: 文件路径    keyWord: 需要修改的文件中所包含的关键字 '''
    f = open(r"D:\项目相关\id.txt", "r")
    lines = f.readlines()  # 读取全部内容
    id = 0
    start = time.clock()
    os.chdir(file)
    items = os.listdir(file)
    print(os.getcwd())
    for name in items:
        print(name)
    #     # 遍历所有文件
        if not os.path.isdir(name):
            new_name = '{}.jpg'.format(lines[id].strip())
            os.renames(name, new_name)
            id += 1
    print('-----------------------分界线------------------------')
    items = os.listdir(file)
    for name in items:
        print(name)

update_file_name(r'D:\项目相关\tx')