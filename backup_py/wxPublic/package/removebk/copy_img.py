from package import *

def copy_imgFile(file_time, filePath, new_filePath):
    try:
        current_folder = os.listdir(filePath)
        # 第二部分，将名称为file的文件复制到名为file_dir的文件夹中
        for x in current_folder:
            if 'white' in x:
                file_dir = r'{}\{}_white.png'.format(new_filePath, file_time)
            elif 'blue' in x:
                file_dir = r'{}\{}_blue.png'.format(new_filePath, file_time)
            else:
                file_dir = r'{}\{}_red.png'.format(new_filePath, file_time)
            #将指定的文件file复制到file_dir的文件夹里面
            shutil.copy("{}\{}".format(filePath, x), file_dir)
        return True
    except:
        return False