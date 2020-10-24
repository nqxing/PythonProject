import time
import requests
# from removebg import RemoveBg
from PIL import Image
import os
from config.fangtang import fangtang

def remove_bg(msg):
    ok_state = []
    file_time = int(time.time())
    flie_path = r'remove_bg\file\{}.jpg'.format(file_time)
    msg.get_file(save_path='{}'.format(flie_path))
    if os.path.exists('{}'.format(flie_path)):
        msg.reply('图片接收成功，正在为您生成底色照片..')
        f = open(r"remove_bg\id.txt", "r", )
        lines = f.readlines()  # 读取全部内容
        for i in range(len(lines)):
            r = get_account(lines[i].strip())
            if r.status_code == 200:
                if r.json()['data']['attributes']['api']['free_calls'] != 0:
                    remove_background_from_img_file(lines[i].strip(), "{}".format(flie_path)) #图片地址
                    if os.path.exists('{}_no_bg.png'.format(flie_path)):
                        im = Image.open('{}_no_bg.png'.format(flie_path))
                        x, y = im.size
                        try:
                            p = Image.new('RGBA', im.size, (255, 255, 255))
                            p.paste(im, (0, 0, x, y), im)
                            p.save(r'remove_bg\file\{}_white.png'.format(file_time))
                            ok_state.append(r'remove_bg\file\{}_white.png'.format(file_time))
                        except:
                            pass
                        try:
                            p = Image.new('RGBA', im.size, (0, 0, 255))
                            p.paste(im, (0, 0, x, y), im)
                            p.save(r'remove_bg\file\{}_blue.png'.format(file_time))
                            ok_state.append(r'remove_bg\file\{}_blue.png'.format(file_time))
                        except:
                            pass
                        try:
                            p = Image.new('RGBA', im.size, (255, 0, 0))
                            p.paste(im, (0, 0, x, y), im)
                            p.save(r'remove_bg\file\{}_red.png'.format(file_time))
                            ok_state.append(r'remove_bg\file\{}_red.png'.format(file_time))
                        except:
                            pass
                        return ok_state
                    else:
                        return '图片处理失败，请确认您分享的是人像图'
                else:
                    fangtang('去除背景api余额不足啦..','去除背景api余额不足啦..')
            else:
                return '出错了，请稍后重试'
    else:
        return '图片接收失败，请稍后重试'


def remove_background_from_img_file(api_key, img_file_path, size="regular"):
    """
    Removes the background given an image file and outputs the file as the original file name with "no_bg.png"
    appended to it.
    :param img_file_path: the path to the image file
    :param size: the size of the output image (regular = 0.25 MP, hd = 4 MP, 4k = up to 10 MP)
    """
    # Open image file to send information post request and send the post request
    API_ENDPOINT = "https://api.remove.bg/v1.0/removebg"
    img_file = open(img_file_path, 'rb')
    response = requests.post(
        API_ENDPOINT,
        files={'image_file': img_file},
        data={'size': size},
        headers={'X-Api-Key': api_key})

    output_file(response, img_file.name + "_no_bg.png")

    # Close original file
    img_file.close()

def output_file(response, new_file_name):
    # If successful, write out the file
    if response.status_code == requests.codes.ok:
        with open(new_file_name, 'wb') as removed_bg_file:
            removed_bg_file.write(response.content)
    # Otherwise, print out the error
    else:
        error_reason = response.json()["errors"][0]["title"].lower()
        print("Unable to save %s due to %s", new_file_name, error_reason)

def get_account(key):
    try:
        headers = {
            "accept": "*/*",
            "X-API-Key": key
        }
        r = requests.get('https://api.remove.bg/v1.0/account', headers = headers)
        return r
    except:
        return None

def get_bg_image(msg):
    results = remove_bg(msg)
    if type(results).__name__ == 'list':
        if results:
            for r in results:
                msg.sender.send_image('{}'.format(r))
        else:
            msg.reply('底色照片生成失败')
    else:
        msg.reply(results)