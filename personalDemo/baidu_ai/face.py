import base64
import json
import requests


class BaiduPicIndentify:
    def __init__(self, img):
        self.AK = "6IHGrudq0uwWlCCp58lYS9yW"
        self.SK = "yc4EIM5wfgXVxMl8k4TyoGGF4qZGfmmo"
        self.img_src = img
        self.headers = {
            "Content-Type": "application/json; charset=UTF-8"
        }

    def get_accessToken(self):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + self.AK + '&client_secret=' + self.SK
        response = requests.get(host, headers=self.headers)
        json_result = json.loads(response.text)
        return json_result['access_token']

    def img_to_BASE64(slef, path):
        with open(path, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            return base64_data

    def detect_face(self):
        # 人脸检测与属性分析
        img_BASE64 = self.img_to_BASE64(self.img_src)
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
        post_data = {
            "image": img_BASE64,
            "image_type": "BASE64",
            "face_field": "gender,age,beauty,gender,face_shape,expression",
            "face_type": "LIVE"
        }
        access_token = self.get_accessToken()
        request_url = request_url + "?access_token=" + access_token
        response = requests.post(url=request_url, data=post_data, headers=self.headers)
        json_result = json.loads(response.text)
        if json_result['error_msg'] != 'pic not has face':
            print("图片中包含人脸数：", json_result['result']['face_num'])
            print("年龄大约：", json_result['result']['face_list'][0]['age'])
            beauty = json_result['result']['face_list'][0]['beauty']
            print("颜值评分：", beauty)
            if beauty <= 30:
                beautys = '难看'
            elif beauty > 30 and beauty <= 60:
                beautys = '一般'
            elif beauty > 60 and beauty <= 80:
                beautys = '好看'
            else:
                beautys = '超好看'
            gender = json_result['result']['face_list'][0]['gender']['type']
            if gender == 'female':
                genders = '女'
            elif gender == 'male':
                genders = '男'
            else:
                genders = '未知'
            print("性别：", genders)
            expression = json_result['result']['face_list'][0]['expression']['type']
            if expression == 'smile':
                expressions = '微笑'
            elif expression == 'laugh':
                expressions = '大笑'
            elif expression == 'none':
                expressions = '不笑'
            else:
                expressions = '未知'
            face_shape = json_result['result']['face_list'][0]['face_shape']['type']
            if face_shape == 'square':
                face_shape = '正方形'
            elif face_shape == 'triangle':
                face_shape = '三角形'
            elif face_shape == 'oval':
                face_shape = '椭圆'
            elif face_shape == 'heart':
                face_shape = '心形'
            elif face_shape == 'round':
                face_shape = '圆形'
            else:
                face_shape = '未知'
            print("人物脸型：", face_shape)
            print("表情：", expressions)
            print("综合评价：", beautys)


if __name__ == '__main__':
    # img_src = input('请输入需要检测的本地图片路径:')
    img_src = r'C:\Users\Administrator\Desktop\微信图片_20200717151737.jpg'
    baiduDetect = BaiduPicIndentify(img_src)
    baiduDetect.detect_face()