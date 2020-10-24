import os
work_path = os.getcwd()
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return files
files = file_name("bytes")
for fi in files:
    file = fi.split(".")[0]
    new_path = r'{}\ogg\{}'.format(work_path, file)
    os.mkdir(new_path)
    os.chdir(new_path)
    os.system(r"{}\tools\bnkextr.exe {}\bytes\{}".format(work_path, work_path, fi))
    if os.listdir(new_path):
        os.system("ren *.wav *.wem")
        cmd_str = "for %%f in (*.wem) do {}\\tools\\ww2ogg.exe %%f --pcb {}\\tools\\packed_codebooks_aoTuV_603.bin".format(work_path, work_path)
        with open("1.bat", "w", encoding='utf-8') as f:
            f.write(cmd_str)
        os.system("1.bat")
        os.system("del *.wem *.bat /s")
    else:
        print('{}文件解压wav格式为空了..'.format(fi))

