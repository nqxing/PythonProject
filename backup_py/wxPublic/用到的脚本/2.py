import shutil
import os
import requests

# def copy_imgFile(file_time, filePath, new_filePath):
#     current_folder = os.listdir(filePath)
#     # 第二部分，将名称为file的文件复制到名为file_dir的文件夹中
#     for x in current_folder:
#         if 'white' in x:
#             file_dir = r'{}/{}_white.png'.format(new_filePath, file_time)
#         elif 'blue' in x:
#             file_dir = r'{}/{}_blue.png'.format(new_filePath, file_time)
#         else:
#             file_dir = r'{}/{}_red.png'.format(new_filePath, file_time)
#         #将指定的文件file复制到file_dir的文件夹里面
#         shutil.copy("{}\{}".format(filePath, x), file_dir)

def remove_background_from_img_file(api_key, img_file_path, size="regular"):
    API_ENDPOINT = "https://api.remove.bg/v1.0/removebk"
    img_file = open(img_file_path, 'rb')
    response = requests.post(
        API_ENDPOINT,
        files={'image_file': img_file},
        data={'size': size},
        headers={'X-Api-Key': api_key})
    print(img_file_path)
    print(img_file.name)
    output_file(response, img_file.name + "_no_bg.png")
    img_file.close()

def output_file(response, new_file_name):
    print(response.status_code, requests.codes.ok)
    # If successful, write out the file
    if response.status_code == requests.codes.ok:
        with open(new_file_name, 'wb') as removed_bg_file:
            removed_bg_file.write(response.content)
    # Otherwise, print out the error
    else:
        print(response.text)
        error_reason = response.json()["errors"][0]["title"].lower()
        print("Unable to save %s due to %s", new_file_name, error_reason)

remove_background_from_img_file("CS59zku7fn5PLjz1yweemQZ8", "1584277651.jpg", size="regular")