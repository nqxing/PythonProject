import requests
import base64
def get_Access_Token():
    # url = 'https://aip.baidubce.com/oauth/2.0/token'
    # dict = {
    #     'grant_type' : 'client_credentials',
    #     'client_id' : 'AdPbZWoxZrE7OlBsY10ARKtA',
    #     'client_secret' : 'mEf4QMcxFvTGX90naVLqVf8GjsTKlllr'
    # }
    # r = requests.post(url,data=dict).json()
    # access_token = r['access_token']
    access_token = '24.ad04a0dfb0af0b465cb2abf5517c2c56.2592000.1557648777.282335-16004002'
    get_64ba(access_token)
def get_64ba(access_token):
    # temp_file = open('captcha.jpg', 'rb')
    # temp_image = temp_file.read()
    # base641 = base64.b64encode(temp_image)
    # base641 = '/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAAYAEADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD1vVU1Od0gsW8lD9+bPI+lY/hsXdvrt7ayzNMijLMe7f5Jrf1NL54ALF0Vwfm39xXP+H7uS3FygtnnuRL++IbnHrzXPPSom7lj9Y1PUpNbXT7BvLZRncO/1q/4f1G6uHntL5lNxAcEjvXOXuoXP/CUyS2ReNig3F4zgD39B71Y8PSNa6tPc31zCPMU5Ibqc1lGr+836/IC7p2qXC6/fpeTuIYgSFY8AfSuhgvre5tTcwvviHcDn8q4u+ewu/F2JLgfZ5FG4hsA1c0e7s9O1u6tkvF+y7dyLnjNVCrZ2b0uA611wQeJp0lupXtWHyBmyoNdXHPFNkRyKxXqAelcC5stQ8UzrPBKBj5ERSC5/pWh4X3W+vXlsokWPbna/XrRSqu9ul2Bp3r65bXskkSC4tiDtROCv19aqeFbG9gur2e6jdGY9G7nrRRW3s/eUrgM1Gx1g6p9vtI/mZdrISCPp9Kl8OW+oi7n+32+2M9N6d/Y+lFFCpJS5rgQ6vbTvrKX+n2wlFt8kiBeQeuMfQg/Qg0nhW3kvb+61S4jXD8IQoxRRWUYJzT9X+gGhc6Vcr4lgv7dFMWMSZOMVV0KJj4m1STPCHaR6E//AKqKKuUVGUbdX+gH/9k='
    base641 = '/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAAYAEADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD0TxDr9xpxjs7e5MkyH965UBiO3TjP0/Sl8JJJDqN4HkZ2nVZWJ6knnn8zVTWrSObUNW8zKyBVkjOOoHWrmg3MbarExZV3Wozz6HFaG3Qs6xNLH4m09fPeGMqQWB4OSMj8cD9K6Esk6OiSexKNyK5DxJGup+ILOzFwEXYW3A0/wgy211fQO5GGwpZsjj39aBW0Fe5vJPG0VsssjRwptOD1BwTn64H5Cur8iMXBnAxIVCEjuBnAP0yfzPrXC6lqctn4lvGtCnmOFUSEjC/jW74ejuow9xe34cydY2YcGgGR+I9Yure7h06yH76YcN3FT6HNrhl8nVIVCBTiTuTUI8i58bhtyuYrfK4OcGukoBnLazDJPrd1DGpaRrLIUDkjOKtaP4etY7OGS8tF+1BNrZ5oooC5AfDMA8RtdfZwbby8he270xU2jaTbtHcNcaeIy0pKq6449qKKBXM+68GIUvnTa7yfNCAOVPpWlomn2k2mRi4skWeP5JFZcEHHf8CD+NFFA7sy9T0S9sNZGoaTCCCAvlqO9bWhx6sFkk1SQEt91B/DRRQK5//Z'
    get_string(base641,access_token)
def get_string(base641,access_token):
    print(access_token)
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    print(str(base641))
    dict = {
        'access_token' : '{}'.format(access_token),
        'image' : '{}'.format(base641),
        'language_type' : 'CHN_ENG'
    }
    r = requests.post(url,headers=headers,data=dict)
    print(r.text)
def test():
    temp_file = open('154.jpg', 'rb')
    temp_image = temp_file.read()
    base641 = base64.b64encode(temp_image)
    print(base641)
get_Access_Token()
# test()