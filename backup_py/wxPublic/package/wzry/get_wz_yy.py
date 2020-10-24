from package import *

def return_wzYy(wz_path, name):
    end_str = '\n\n<a href="https://mp.weixin.qq.com/s/9WY90GBIk2HlmvJWSxScLA">点此加入王者壁纸开黑群了解更多游戏动态</a>'
    try:
        if name == 'oth' or name == 'OTH' or name == 'Oth':
            return '恭喜~ 找到了({})的语音包合集，该合集是大厅bgm、峡谷野怪和快捷信号等其他游戏中听到的所有音效，语音较多建议先保存至自己的网盘，' \
                   '再打开APP在线试听后选择下载哦~\n\n百度网盘：<a href="https://pan.baidu.com/s/13Be_doaW66KWfSYPCC2Y5g">点我下载</a>【提取码：tv61】'.format(name)+end_str
        else:
            conn = sqlite3.connect(wz_path)
            # 创建一个游标 curson
            cursor = conn.cursor()
            cursor.execute("SELECT yx_name,yy_url FROM hero_yy WHERE yx_name LIKE '%" + "{}".format(name) + "%'")
            results = cursor.fetchall()
            # 关闭cursor/链接
            cursor.close()
            if conn:
                conn.close()
            if len(results) != 0:
                result = '恭喜~ 找到了({})的皮肤语音包合集，因英雄皮肤语音较多建议先保存至自己的网盘，再打开APP在线试听后选择下载哦~\n\n'.format(name)
                for i in range(len(results)):
                    strs = '{}：{}\n\n'.format(results[i][0], results[i][1])
                    result += strs
                return result.strip()+end_str
            else:
                return "没有找到({})的皮肤语音包，请确认名字输入正确哦~ 若要获取其他资源，请先发送“指令”切换哦".format(name)+end_str
    except:
        return "抱歉~ 查询出错了，请重试~"+end_str