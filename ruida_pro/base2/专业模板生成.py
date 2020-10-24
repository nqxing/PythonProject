import xlrd
from xlutils.copy import copy
from IQ.base2.initialData import *
def MajorTemplate():
    xls = xlrd.open_workbook(r'基础模板\空\专业模板(空).xls', formatting_info=True)
    xlsc = copy(xls)
    sheet = xlsc.get_sheet(0)
    # i既是lis的下标，也代表每一列#处理表头
    for num in range(len(Major)):
        new_row = num + 1  # 因为循环的时候 是从0开始循环的，第0行是表头，不能写
        # 要从第二行开始写，所以这里行数要加1
        sheet.write(new_row, 0, Major[num])
        sheet.write(new_row, 1, 'Z-{}'.format(num+1))
        sheet.write(new_row, 2, num+1)
        sheet.write(new_row, 3, Majorintroduce[num])
    xlsc.save('基础模板\\专业模板.xls')
    print('专业模板生成成功~~')
MajorTemplate()