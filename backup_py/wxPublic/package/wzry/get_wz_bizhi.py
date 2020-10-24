from package import *

def return_wzSkin(wz_path, name):
    end_str = '\n\n<a href="https://mp.weixin.qq.com/s/9WY90GBIk2HlmvJWSxScLA">点此加入王者壁纸开黑群了解更多游戏动态</a>'
    try:
        if name == 'all' or name == 'ALL' or name == 'All':
            return '王者荣耀全英雄皮肤壁纸（2020-03-10更新，391张）\n\n百度网盘：<a href="https://pan.baidu.com/s/1k5PVC7oTMy-vbgJUxeAsJQ">点我下载</a> 【提取码：7rf7】'+end_str
        else:
            conn = sqlite3.connect(wz_path)
            # 创建一个游标 curson
            cursor = conn.cursor()
            cursor.execute("SELECT pf_name, dwz_url FROM pf_link WHERE pf_name LIKE '%" + "{}".format(name) + "%'")
            results = cursor.fetchall()
            # 关闭cursor/链接
            cursor.close()
            if conn:
                conn.close()
            if len(results) != 0:
                result = '找到了{}张({})的壁纸:\n\n'.format(len(results), name)
                for i in range(len(results)):
                    strs = '{}\n{}\n\n'.format(results[i][0], results[i][1])
                    result += strs
                result = result.strip()
                if len(result) > 1365:
                    return '该关键字信息量太大了，请换个详细点的关键字吧'+end_str
                return result+end_str
            else:
                return "没有找到({})的壁纸，请确认名字输入正确哦~ 若要获取其他资源，请先发送“指令”切换哦".format(name)+end_str
    except:
        return "抱歉~ 查询出错了，请重试~"+end_str