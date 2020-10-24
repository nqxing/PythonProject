import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49'
                  ' Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080'
}

# def sms_token(mobile):
#     restr = """
#     phoneCode=86&loginId={}&countryCode=CN&ua=122%23DVpsyDX3EExzH4pZMEpJEJponDJE7SNEEP7rEJ%2B%2Ff9t%2F2oQLpo7iEDpWnDEeK51HpyGZp9hBuDEEJFOPpC76EJponDJL7gNpEPXZpJRgu4Ep%2BFQLpoGUEELWn4yP7SQEEyuLpERxVWf3prZCnaRx9kb%2Fb2g0gQ9kUWE8kmLjcq25jeeqQggNLwsp8YQbQh%2B0WEVDrN11%2FM%2FttQoWfusL2slOek%2FU8nF10Dr1WjYwQrJhLLFnEoGAR8VAIVGDqMfEessGoWp1uOpQQ3Oq8o%2BUJDEEyB3tqWZ0HsO8ngL4uO8pELVZGWZRfsTbyFfDmSfbEEpMnMp1uOIEELXZ8oL6JNEERBfmqM32E5pangL4ul0EDLVr8CpUJ4bEyNRDqMfVpNpnngp1ul6PxhIiaO7ftq5PMYJPOXVpZSR81PRo7Xqb0jnDgw%2FFhwpE6BJHDWC0daUaKjFztBZNjHuhQP0ybzFN6JRuefGPzE2i2wizaaf%2FOR%2Bak9s%2BsmBkhplNd4PuXeO7nvP9jLvMjbWkoK7GUxW0Fx4WqKfKULxqJWFdYZ7rdKz5RwklwHyuSyOTbVYENfLt4Q4usNHTMshMzieJulowjAAiTjJHEgqIuJPlvpQTOSyNmqKLRLrMGtw%2Fh%2BYdrSiaTjqbRAqaoz5KMz4dmP0axAmcNztJn4dvy5ZGlxEsiG0t7eaMePuTZGCKwGmlr4CsVQSr2gkTvIHcCUOGV9tYqT5tcRCHzOoJ5mRnc8qEbjcv8%2FOFr8xwrjW2vYarqbPDn4Xd8dIKCB62LbcDz4T3BNVbcdGPrIbaRz0uD0txR6R8Mbd8khiGXFXO4cuH0ONWW8IGTNBbjaW%2BexVKM2rLxtEkgQr3boVYQ0JLSlaB4tnBdunxhYxFF8Q0UCqSIrpE8MBwdj5CoWo3BLDiG1C7TuC6m8K1bDdunfVPBr3vs9ZPSUJuqnf%2FbJnDPvRapWUMJYpnE7smpoEgPuNh%2BF%2BLAkEtCxm9isCB88vwD6BMb2M%2BLA60lpaafdXi%2FeXkY6n6iQiYa0uMoMp9wS%2B0ne9OdZx%2FzrtwcgUAsPKTSTZWDkLiNecQfKm3rVMRcYjgvstrGVJX4s4%2FdKQ2LaJyo5kFD%2FBwTBi4jKjXAJ%2B8awuZF1KLyyyVEpccwK%2FzN1qOkP0hv9%2B91c2U0P2%2BtPJOZy9SX6GeqbjvRD%3D%3D&umidGetStatusVal=255&screenPixel=1920x1080&navlanguage=zh-CN&navUserAgent=Mozilla%2F5.0%20%28Windows%20NT%206.1%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F81.0.4044.92%20Safari%2F537.36&navPlatform=Win32&appName=eleme&appEntrance=eleme_sms_h5&_csrf_token=OHKb7Zp6YWEtIsQII1c4iA&umidToken=3f1db554bd603f2da7c5c5dd81ca941c9d433c2f&isMobile=false&lang=zh_CN&returnUrl=&hsiz=18dd12111fd4d1c0d8109c441a7c17a8&fromSite=25&bizParams=
#     """
#     url = "https://ipassport.ele.me/newlogin/sms/send.do?appName=eleme&fromSite=25"
#     r = requests.post(url, headers=HEADERS, params=restr.format(mobile), verify=False)
#     print(r.text)
#
# def get_sid(sms_token, mobile, sms_code):
#     restr = """
#     loginId={}&phoneCode=86&countryCode=CN&smsCode={}&smsToken={}&keepLogin=false&ua=122%23tXKkAJjmEE%2BJODpZMEpJEJponDJE7SNEEP7rEJ%2B%2Ff9t%2F2oQLpo7iEDpWnDEeK51HpyGZp9hBuDEEJFOPpC76EJponDJL7gNpEPXZpJRgu4Ep%2BFQLpoGUEELWn4yP7SQEEyuLpERdVt1%2FprZCnaRx9kb%2FCn4cJdyss9WK8RAWEzopC1tJqJ0lVxV3SvrjG0mO0C8gMgZ7ccfjmyseD88anEK08QYrrZvWGHIxhbXOgO3R8dmpI53uwtaXRArzJ29xlipR8N3HIYGDqMfpessGoX2Suy0EDLWKp9NXYYQpyBvmqM3bD5pMngaHOkPtDLVr8oRfJDEERgMdt1%2BoEEpxkMp1ul5bDRXZ8oL6JNEEyBfDqMfbDDpanSL4ul0EDLVr8CpUJ4bEyF3mqW32E9vxnSpvGOjWDLXZ8CmmBEp6ny1kfiAspn8PtHwoZSR81PRo7Xqb0jnDgw%2FFhwpE64U5ER8gDjw9mSqbn%2FC%2BuJrG7GkMpIo6oLAhJLc3xEp2GGMqLAG%2FoakDYO6A97AG5shZbRwo27kbmeB%2B%2BItuLnblHQ2iK%2FzECxXoYVklnUB0msbhVEX9Yy3Ew%2B1QogTIYQz97OBOjNY66hch21Xm0nNdlFlukYl7byboOiAD2pk3aUjxgJ%2BzBEgZvqQsU1E7M76fWBc6bW%2BCXsx246L%2FSyfgfJRjF%2FMCB0fadno7j1W5qsSnAZCSBxgUYHyzWoFpC7sYX8e6DHBKsd9a8Wylx%2F89PxDFPr7X1D1wn0W8dKtGsJyQ2jnuAKdjfwdOyj%2B8Du07VKm%2FHXCYXH3K%2FbD%2Byxu1UHpS8FQmri0aLozzJZ2fLn279vEV0XnjirEpCOwZJOuxWq5t%2BOo0uFTJkDc8kb%2Ft5SmoeJli7qak7ERqJfz1n7Bh8J6YBWIFZPLX8KwPpG5KxpfqI2%2BoD%2Bmue0ipOkq86wuhPFiEUVIjIYFeNgvorWLTqqfXGGyJYAgbbhLfdgEEFqQal6FNN6UdEvTwAXtRfNKKS%2F3qpNWaU3fZcB0YSKYcCu3oKSDdqzUYQF0hpGMxAhNJZ5ouuu56n8QYfwBSFr%2FNuCaIG58l%2Bjz8iQ7IirgkEqSj50KsLieyrMVqb5t6J%2B1xw1Bb1YRUPlmnZgqQBK%2Bp2MAldT917b4DBUOWbogF1YyRntfqi%2FGql%2FrIrT0PjHoQw66qriqMB%2FgQORMW%2FoITigqMKq6wpEQ79RWYYJLnjpWRGI5RmUsEMtTyRIAowGYfctSBAAj4FqvAVq0%3D&umidGetStatusVal=255&screenPixel=1920x1080&navlanguage=zh-CN&navUserAgent=Mozilla%2F5.0%20%28Windows%20NT%206.1%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F81.0.4044.92%20Safari%2F537.36&navPlatform=Win32&appName=eleme&appEntrance=eleme_sms_h5&_csrf_token=OHKb7Zp6YWEtIsQII1c4iA&umidToken=3f1db554bd603f2da7c5c5dd81ca941c9d433c2f&isMobile=false&lang=zh_CN&returnUrl=&hsiz=18dd12111fd4d1c0d8109c441a7c17a8&fromSite=25&bizParams=
#     """
#     url = "https://ipassport.ele.me/newlogin/sms/login.do?appName=eleme&fromSite=25&"
#     r = requests.post(url, params=restr.format(mobile, sms_code, sms_token))
#     print(r.text)
#
# sms_token("17134502947")
# get_sid("", "15160654911", "")

mobile_send_code_url = 'https://h5.ele.me/restapi/eus/login/mobile_send_code'
dict = {"scf": "ms", "mobile": "15160654911"}
r = requests.post(mobile_send_code_url, headers=HEADERS, data=dict, timeout=25)
print(r.status_code, r.text)