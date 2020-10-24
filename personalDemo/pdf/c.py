import requests
from lxml import etree
import re
import os
import pdfkit


def gethtml(url, encode):
    r = requests.get(url)
    r.encoding = encode
    return r.text


def writehtml(path, str):
    f = open(path, 'w+', encoding='utf-8')
    f.write(str)
    f.close


def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"
    new_title = re.sub(rstr, "_", title)
    return new_title


def mkdir(path):
    path = path.strip()
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        print('文件夹已存在，请检查后再试！')
        return False


def getdata(url, pdf):
    print('开始获取,请稍候...')
    c_url = url.split('/')[0] + '//' + url.split('/')[2] + '/'
    html = gethtml(url, 'utf-8')
    ehtml = etree.HTML(html)
    urll1 = ehtml.xpath('//*[@id="contents"]/dd/a/@href')
    till1 = ehtml.xpath('//*[@id="contents"]/dd/a/text()')
    s = ehtml.xpath('//*[@id="contents"]/dd/span/text()')
    folder = validateTitle(ehtml.xpath('//*[@id="contents"]/dt/a/text()')[0])
    if mkdir(savepath + folder):
        m = 0
        txt = ''
        for i in urll1:
            html = gethtml(c_url + i, 'utf-8')
            ehtml = etree.HTML(html)
            strs = ehtml.xpath('//*[@id="article"]')[-1]
            txtl1 = etree.tostring(strs, encoding="utf-8", pretty_print=True, method="html").decode("utf-8")
            fname = validateTitle(s[m] + ' ' + till1[m])
            txtl1 = re.sub('<h1>.*?</h1>', '<h1>' + fname + '</h1>', txtl1)
            txtl1 = re.sub('src="/', 'src="' + c_url + '/', txtl1)
            txt = txt + txtl1
            # writehtml(savepath+folder+'\\'+fname+'.html', txtl1)  #每个章节生成一个html文件
            s1 = ehtml.xpath('//*[@id="contents"]/dl/dd/text()')
            s2 = ehtml.xpath('//*[@id="contents"]/dl/dd/a/text()')
            urll2 = ehtml.xpath('//*[@id="contents"]/dl/dd/a/@href')
            print(fname)
            n = 0
            for j in urll2:
                html = gethtml(c_url + j, 'utf-8')
                ehtml = etree.HTML(html)
                strs = ehtml.xpath('//*[@id="arc-body"]')[-1]
                txtl2 = etree.tostring(strs, encoding="utf-8", pretty_print=True, method="html").decode("utf-8")
                fname = validateTitle(s1[n] + ' ' + s2[n])
                txtl2 = re.sub('<h[2,4]>', '<h3>', txtl2)
                txtl2 = re.sub('</h[2,4]>', '</h3>', txtl2)
                txtl2 = re.sub('src="/', 'src="' + c_url + '/', txtl2)
                txtl2 = '<h2>' + fname + '</h2>' + txtl2
                txt = txt + txtl2
                # writehtml(savepath+folder+'\\'+fname + '.html', txtl2) #每个章节生成一个html文件
                print(fname)
                n += 1
            m += 1
        writehtml(savepath + folder + '\\' + folder + '.html', txt)
        if pdf:
            print('开始生成pdf,请稍候...')
            path_wk = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # wkhtmltopdf安装位置
            config = pdfkit.configuration(wkhtmltopdf=path_wk)
            options = {
                'page-size': 'A4',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'outline': None
            }
            pdfkit.from_file([savepath + folder + '\\' + folder + '.html'], savepath + folder + '\\' + folder + '.pdf',
                             options=options, configuration=config)
        print('任务完成!')


if __name__ == '__main__':
    url = 'http://c.biancheng.net/python/'  # 获取教程url地址
    savepath = 'C:\\'  # 保存位置
    getdata(url, True)  # 后面True表示生成PDF，False不生成