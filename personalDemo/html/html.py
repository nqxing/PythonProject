f = open("mb.txt", "r",)   #设置文件对象
strs = f.read()     #将txt文件的所有内容读入到字符串str中
f.close()   #将文件关闭
# print(strs)
html = '''
<p style="white-space: normal;"><span style="font-size: 14px;color: rgb(136, 136, 136);"><img data-ratio="0.1" data-src="https://mmbiz.qpic.cn/mmbiz_gif/Qa7qwBRw0Cxr3D7LibzVwFn0wqKACZSxklHUuNmczwmtgsD5j2U9QVs6mQCwrUzyBLiatfKNx9DAKicHDiaOZSWdYg/640?wx_fmt=gif" data-type="gif" data-w="1000" style="white-space: normal; font-size: 16px; color: rgb(62, 62, 62); overflow-wrap: break-word !important; box-sizing: border-box !important; visibility: visible !important; width: auto !important; height: auto !important;" _width="auto" class=" __bg_gif" src="./testtesttesttesttesttest_files/640" data-order="0" alt="图片" data-fail="0"></span></p>
					
					
					<p style="white-space: normal;"><br></p>
					<p style="white-space: normal;"><span style="font-size: 14px;color: rgb(136, 136, 136);">“我叫澜，魏都刺客，这次的目标，是一个叫蔡文姬的小孩”</span></p>
					<p style="white-space: normal;"><br></p>
					<p style="white-space: normal;"><span style="font-size: 14px;color: rgb(136, 136, 136);">我没见过她，但我知道，她叫蔡文姬，只是个小孩子，而我是要杀了她的。</span></p>
					<p style="white-space: normal;"><span style="font-size: 14px;color: rgb(136, 136, 136);">我是刺客，我的剑出鞘就要见血，这是我的使命，也是我的宿命......</span></p>
					<p><br></p>
					<p style="white-space: normal;"><span style="font-size: 14px;"><strong style="font-size: 20px;max-width: 100%;color: rgb(217, 33, 66);letter-spacing: 0.544px;background-color: rgb(255, 255, 255);box-sizing: border-box !important;overflow-wrap: break-word !important;">英雄价格：</strong></span></p>
					<p style="white-space: normal;"><span style="font-size: 14px;">18888金币或者488点券（限时）直接购买，也可通过碎片商城通过68英雄碎片进行兑换，18888金币或者488点券（限时）直接购买，也可通过碎片商城通过68英雄碎片进行兑换</span></p>
					<p style="white-space: normal;"><img data-ratio="0.47368421052631576" data-src="https://mmbiz.qpic.cn/mmbiz_jpg/CFpeqnV0qt7dElNauWiaibV0xkCEcfMF0vjvGicGqbxhzZicZNC1cXbnIx7TvmhjH3TeByuhGxCLmNQ6kvUZpxJazA/640?wx_fmt=jpeg" data-type="jpeg" data-w="2280" style="margin-top: 12px; margin-bottom: 12px; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); border-width: 0px; border-style: initial; border-color: initial; user-select: none; border-radius: 0.13333rem; display: block; width: 591.031px !important; height: auto !important; visibility: visible !important;" _width="591.031px" class="" src="https://mmbiz.qpic.cn/mmbiz_jpg/CFpeqnV0qt7dElNauWiaibV0xkCEcfMF0vjvGicGqbxhzZicZNC1cXbnIx7TvmhjH3TeByuhGxCLmNQ6kvUZpxJazA/640?wx_fmt=jpeg" crossorigin="anonymous" alt="图片" data-fail="0"></p>
					<p style="white-space: normal;"><br></p>
					<p style="white-space: normal;"><span style="font-size: 14px;"><strong style="font-size: 20px;max-width: 100%;color: rgb(217, 33, 66);letter-spacing: 0.544px;background-color: rgb(255, 255, 255);box-sizing: border-box !important;overflow-wrap: break-word !important;">技能解析：</strong></span></p>
					<p style="white-space: normal;"><span style="font-size: 14px;">【被动技能：猎杀】</span></p>
					<p><br></p>
					
					                    <p style="white-space: normal;"><span style="font-size: 14px;color: rgb(136, 136, 136);"><img data-ratio="0.1" data-src="https://mmbiz.qpic.cn/mmbiz_gif/Qa7qwBRw0Cxr3D7LibzVwFn0wqKACZSxklHUuNmczwmtgsD5j2U9QVs6mQCwrUzyBLiatfKNx9DAKicHDiaOZSWdYg/640?wx_fmt=gif" data-type="gif" data-w="1000" style="white-space: normal; font-size: 16px; color: rgb(62, 62, 62); overflow-wrap: break-word !important; box-sizing: border-box !important; visibility: visible !important; width: auto !important; height: auto !important;" _width="auto" class=" __bg_gif" src="./testtesttesttesttesttest_files/640" data-order="0" alt="图片" data-fail="0"></span></p>
					<p style="white-space: normal;"><br></p>
					<p style="white-space: normal;"><span style="font-size: 14px;color: rgb(136, 136, 136);">“我叫澜，魏都刺客，这次的目标，是一个叫蔡文姬的小孩”</span></p>
					<p style="white-space: normal;"><br></p>
					<p style="white-space: normal;"><span style="font-size: 14px;color: rgb(136, 136, 136);">我没见过她，但我知道，她叫蔡文姬，只是个小孩子，而我是要杀了她的。</span></p>
					<p style="white-space: normal;"><span style="font-size: 14px;color: rgb(136, 136, 136);">我是刺客，我的剑出鞘就要见血，这是我的使命，也是我的宿命......</span></p>
					<p><br></p>
					<p style="white-space: normal;"><span style="font-size: 14px;"><strong style="font-size: 20px;max-width: 100%;color: rgb(217, 33, 66);letter-spacing: 0.544px;background-color: rgb(255, 255, 255);box-sizing: border-box !important;overflow-wrap: break-word !important;">英雄价格：</strong></span></p>
					<p style="white-space: normal;"><span style="font-size: 14px;">18888金币或者488点券（限时）直接购买，也可通过碎片商城通过68英雄碎片进行兑换</span></p>
					<p style="white-space: normal;"><img data-ratio="0.47368421052631576"  data-w="2280" style="margin-top: 12px; margin-bottom: 12px; -webkit-tap-highlight-color: rgba(0, 0, 0, 0); border-width: 0px; border-style: initial; border-color: initial; user-select: none; border-radius: 0.13333rem; display: block; width: 591.031px !important; height: auto !important; visibility: visible !important;" _width="591.031px" class="" src="https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/528/528-bigskin-1.jpg" crossorigin="anonymous" alt="图片" data-fail="0"></p>
					<p style="white-space: normal;"><br></p>
					<p style="white-space: normal;"><span style="font-size: 14px;"><strong style="font-size: 20px;max-width: 100%;color: rgb(217, 33, 66);letter-spacing: 0.544px;background-color: rgb(255, 255, 255);box-sizing: border-box !important;overflow-wrap: break-word !important;">技能解析：</strong></span></p>
					<p style="white-space: normal;"><span style="font-size: 14px;">【被动技能：猎杀】</span></p>
					<p><br></p>
'''

new_html = strs.replace('{#title#}', '王者庄小周a啊')
new_html = new_html.replace('{#content#}', html)
# data = {'title':'My Home Page','text':'html'}
with open('new.html', 'w', encoding='utf-8') as f:    #设置文件对象
    f.write(new_html)
# print(strs.format('title', html))