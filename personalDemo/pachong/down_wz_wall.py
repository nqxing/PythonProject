import os
import requests
import traceback
import pymysql

def down_wall(skin_name, skin_url, mob_skin_url, hero_name, game, skin_size):
    try:
        if game == 'wzry':
            save_path = r'D:\王者荣耀\{}'
        elif game == 'yxlm':
            save_path = r'D:\英雄联盟\{}'
        else:
            save_path = r'static\wall'
        if '掌盟#' in hero_name:
            hero_name = "掌盟壁纸合集"
        hero_path = save_path.format(hero_name)
        folder = os.path.exists(hero_path)
        if not folder:
            os.makedirs(hero_path)
        if '/' in skin_name:
            skin_name = skin_name.replace('/', '')
        if '\\' in skin_name:
            skin_name = skin_name.replace('\\', '')
        if game == 'yxlm':
            if skin_size != None:
                skin_path = r'{}\{} {}.jpg'.format(hero_path, skin_name, skin_size)
            else:
                skin_path = r'{}\{}.jpg'.format(hero_path, skin_name)
            if not os.path.exists(skin_path):
                img = requests.get(skin_url)
                with open(skin_path, "wb") as f:
                    f.write(img.content)
        elif game == 'wzry':
            skin_path = r'{}\[电脑] {}.jpg'.format(hero_path, skin_name)
            if not os.path.exists(skin_path):
                if skin_url != None:
                    img = requests.get(skin_url)
                    with open(skin_path, "wb") as f:
                        f.write(img.content)
            mob_skin_path = r'{}\[手机] {}.jpg'.format(hero_path, skin_name)
            if not os.path.exists(mob_skin_path):
                if mob_skin_url != None:
                    img = requests.get(mob_skin_url)
                    with open(mob_skin_path, "wb") as f:
                        f.write(img.content)
        else:
            pass
    except:
        print(traceback.format_exc())

mysql_conn = pymysql.connect(host="116.62.126.139", user="root", password="mm123456", port=3306, db='public')
mysql_cursor = mysql_conn.cursor()  # 获取游标

# mysql_cursor.execute("select * from pub_wz_wall")
# values = mysql_cursor.fetchall()
# for v in values:
#     down_wall(v[1], v[2], v[7], v[3], 'wzry', None)

mysql_cursor.execute("select * from pub_lol_wall")
values = mysql_cursor.fetchall()
for v in values:
    down_wall(v[1], v[2], None, v[3], 'yxlm', None)