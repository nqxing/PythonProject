from auto_reply.package import *
from .ident_photo_load import copy_imgFile
from auto_reply.models import pubIdentID

class my_thread(threading.Thread):
    def __init__(self, fromUser, pic_url, file_time, file_names):
        threading.Thread.__init__(self)
        self.fromUser = fromUser
        self.pic_url = pic_url
        self.file_time = file_time
        self.file_names = file_names
    def run(self):
        remove_bg(self.fromUser, self.pic_url, self.file_time, self.file_names)
def remove_bg_index(fromUser, pic_url, file_time, file_names):
    th = my_thread(fromUser, pic_url, file_time, file_names)  # id, name
    th.start()

def remove_bg(fromUser, pic_url, file_time, file_names):
    try:
        flie_path = COPY_IMG_PATH.format('{}.jpg'.format(file_time))
        if dow_image(pic_url, flie_path):
            if os.path.exists('{}'.format(flie_path)):
                lines = pubIdentID.objects.all()
                for i in range(len(lines)):
                    r = get_account(lines[i].api_key.strip())
                    if r != None:
                        if r.status_code == 200:
                            if r.json()['data']['attributes']['api']['free_calls'] != 0:
                                remove_background_from_img_file(lines[i].api_key.strip(), "{}".format(flie_path)) #图片地址
                                if os.path.exists('{}_no_bg.png'.format(flie_path)):
                                    im = Image.open('{}_no_bg.png'.format(flie_path))
                                    x, y = im.size
                                    try:
                                        p = Image.new('RGBA', im.size, (255, 255, 255))
                                        p.paste(im, (0, 0, x, y), im)
                                        p.save(r'{}/{}'.format(NEW_COPY_IMG_PATH, file_names[0]))
                                    except:
                                        pass
                                    try:
                                        p = Image.new('RGBA', im.size, (0, 0, 255))
                                        p.paste(im, (0, 0, x, y), im)
                                        p.save(r'{}/{}'.format(NEW_COPY_IMG_PATH, file_names[1]))
                                    except:
                                        pass
                                    try:
                                        p = Image.new('RGBA', im.size, (255, 0, 0))
                                        p.paste(im, (0, 0, x, y), im)
                                        p.save(r'{}/{}'.format(NEW_COPY_IMG_PATH, file_names[2]))
                                    except:
                                        pass
                                else:
                                    write_log(3, "用户 [{}] 在生成证件照动作 去除背景图时出错了，有可能是分享的不是人像图".format(fromUser))
                                    copy_imgFile(file_time, COPY_IMG_PATH.format("notcon"), NEW_COPY_IMG_PATH)
                            else:
                                send_fqq('去除背景api余额不足啦')
                        else:
                            write_log(1, "用户 [{}] 在生成证件照动作 查询api余额出错了".format(fromUser))
                            copy_imgFile(file_time, COPY_IMG_PATH.format("error"), NEW_COPY_IMG_PATH)
                    else:
                        write_log(3, "用户 [{}] 在生成证件照动作 查询api余额出错了".format(fromUser))
                        copy_imgFile(file_time, COPY_IMG_PATH.format("error"), NEW_COPY_IMG_PATH)
            else:
                write_log(3, "用户 [{}] 在生成证件照动作 图片下载失败了".format(fromUser))
                copy_imgFile(file_time, COPY_IMG_PATH.format("error"), NEW_COPY_IMG_PATH)
        else:
            write_log(3, "用户 [{}] 在生成证件照动作 图片下载失败了".format(fromUser))
            copy_imgFile(file_time, COPY_IMG_PATH.format("error"), NEW_COPY_IMG_PATH)
    except:
        write_log(3, format(traceback.format_exc()))
        copy_imgFile(file_time, COPY_IMG_PATH.format("error"), NEW_COPY_IMG_PATH)
        send_fqq('生成证件照出错了，快去看看吧')

def dow_image(img_url, img_path):
    try:
        headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
        }
        img = requests.get(img_url, headers=headers)
        with open(r"{}".format(img_path), "wb") as f:
            f.write(img.content)
        return True
    except:
        write_log(3, traceback.format_exc())
        return False
def remove_background_from_img_file(api_key, img_file_path, size="regular"):
    API_ENDPOINT = "https://api.remove.bg/v1.0/removebg"
    img_file = open(img_file_path, 'rb')
    response = requests.post(
        API_ENDPOINT,
        files={'image_file': img_file},
        data={'size': size},
        headers={'X-Api-Key': api_key})
    output_file(response, img_file.name + "_no_bg.png")
    img_file.close()

def output_file(response, new_file_name):
    # If successful, write out the file
    if response.status_code == requests.codes.ok:
        with open(new_file_name, 'wb') as removed_bg_file:
            removed_bg_file.write(response.content)
    # Otherwise, print out the error
    else:
        write_log(3, response.text)
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
        write_log(3, traceback.format_exc())
        return None