import asyncio
from pyppeteer import launch
import time
async def main():
    browser= await launch(headless=False,userDataDir='./userdata',args=['--disable-infobars'])
    page=await browser.newPage()

    await page.setViewport({'width': 400, 'height': 768})
    await page.setUserAgent(
        'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080')
    url = 'https://h5.ele.me/hongbao/#is_lucky_group=true&device_id=&theme_id=569&sn=2a7a9095ea2a98bd.2&hardware_id=&platform=4&lucky_number=0'

    sss = {'domain': '.ele.me', 'httpOnly': False, 'name': 'snsInfo[101204453]', 'path': '/', 'secure': True,
           'value': '%7B%22city%22%3A%22%E5%8E%A6%E9%97%A8%22%2C%22constellation%22%3A%22%22%2C%22eleme_key%22%3A%220ceb2557e771603ab407f9b618ffd284%22%2C%22figureurl%22%3A%22http%3A%2F%2Fqzapp.qlogo.cn%2Fqzapp%2F101204453%2F969C874F3DAFCBDE2E48EEA12E9A87D3%2F30%22%2C%22figureurl_1%22%3A%22http%3A%2F%2Fqzapp.qlogo.cn%2Fqzapp%2F101204453%2F969C874F3DAFCBDE2E48EEA12E9A87D3%2F50%22%2C%22figureurl_2%22%3A%22http%3A%2F%2Fqzapp.qlogo.cn%2Fqzapp%2F101204453%2F969C874F3DAFCBDE2E48EEA12E9A87D3%2F100%22%2C%22figureurl_qq%22%3A%22http%3A%2F%2Fthirdqq.qlogo.cn%2Fg%3Fb%3Doidb%26k%3DialyhpDO4FW4icQicuj0ia2kVg%26s%3D640%26t%3D1556538515%22%2C%22figureurl_qq_1%22%3A%22http%3A%2F%2Fthirdqq.qlogo.cn%2Fg%3Fb%3Doidb%26k%3DialyhpDO4FW4icQicuj0ia2kVg%26s%3D40%26t%3D1556538515%22%2C%22figureurl_qq_2%22%3A%22http%3A%2F%2Fthirdqq.qlogo.cn%2Fg%3Fb%3Doidb%26k%3DialyhpDO4FW4icQicuj0ia2kVg%26s%3D100%26t%3D1556538515%22%2C%22figureurl_type%22%3A%221%22%2C%22gender%22%3A%22%E5%A5%B3%22%2C%22gender_type%22%3A1%2C%22is_lost%22%3A0%2C%22is_yellow_vip%22%3A%220%22%2C%22is_yellow_year_vip%22%3A%220%22%2C%22level%22%3A%220%22%2C%22msg%22%3A%22%22%2C%22nickname%22%3A%22%E5%B0%91%E5%B9%B4%E6%A2%A6%E4%BB%96%E5%9F%8E%E3%80%81%22%2C%22openid%22%3A%22969C874F3DAFCBDE2E48EEA12E9A87D3%22%2C%22province%22%3A%22%E7%A6%8F%E5%BB%BA%22%2C%22ret%22%3A0%2C%22vip%22%3A%220%22%2C%22year%22%3A%221996%22%2C%22yellow_vip_level%22%3A%220%22%2C%22name%22%3A%22%E5%B0%91%E5%B9%B4%E6%A2%A6%E4%BB%96%E5%9F%8E%E3%80%81%22%2C%22avatar%22%3A%22http%3A%2F%2Fthirdqq.qlogo.cn%2Fg%3Fb%3Doidb%26k%3DialyhpDO4FW4icQicuj0ia2kVg%26s%3D40%26t%3D1556538515%22%7D'}
    # await page.setCookie(sss)
    await page.goto(url)
    # await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    # await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    # await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

    await page.setCookie(sss)
    time.sleep(3000)
    await page.goto(url)

    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')  # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
    # await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    # await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    # await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')
    # await page.cookies(url)
    await asyncio.sleep(1000)

asyncio.get_event_loop().run_until_complete(main())