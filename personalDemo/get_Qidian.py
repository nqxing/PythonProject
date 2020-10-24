import requests
import re
id = 1
def get_txt(url):
    headers = {
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0; Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106Safari / 537.36',
    }
    try:
        global id
        id+=1
        r = requests.get(url,headers=headers).text
        chapterName_zz = re.compile('<h3 class="j_chapterName">(.*?)</h3>',re.S)
        content_zz = re.compile('<div class="read-content j_readContent">(.*?)</div>',re.S)
        chapterNext_zz = re.compile('<a id="j_chapterNext" href="(.*?)"',re.S)
        chapterName = re.findall(chapterName_zz,r)
        content = re.findall(content_zz,r)
        content = "".join(content[0].split())
        contentlist = content.split('<p>')
        contentlist.remove('')
        # del contentlist[0]
        # del contentlist[-1]
        content = "\n    ".join(str(c) for c in contentlist)
        chapterNext = re.findall(chapterNext_zz,r)
        content_txt = chapterName[0] +'\n    '+ content+'\n\n'
        sava_txt(content_txt,chapterNext)
    except Exception as e:
        print('出错了~~',e)
def sava_txt(content_txt,chapterNext):
    with open('txt.txt', 'a', encoding='utf-8') as file:
        file.write(content_txt)
    url = 'https:' + chapterNext[0]
    print(id,' ',url)
    get_txt(url)
def main():
    url = 'https://read.qidian.com/chapter/UtGr9-X1c1bmkXioLmMPXw2/q2wvL7je_d76ItTi_ILQ7A2'
    get_txt(url)
if __name__ == '__main__':
    main()