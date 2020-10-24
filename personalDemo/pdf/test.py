import pdfkit
f = open("1.txt", "r")
lists = list(f.readlines())
html = '<html><head><meta charset="UTF-8"></head>%s</html>'%lists[0]
# html = lists[0]
config=pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
options = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'outline': None
}
# pdfkit.from_url('http://www.baidu.com', 'url_test.pdf',configuration=config) #通过url地址生成
pdfkit.from_string(html,'string_test1.pdf',configuration=config)
# pdfkit.from_file('xxx.html','file_test.pdf',configuration=config)