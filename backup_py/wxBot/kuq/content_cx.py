from config.config import CX_MIN

def cx_content(kq_cursor, ticks):
    # 查询酷Q聊天记录库
    # kq_cursor.execute('''select content from event where time > %s and type is not Null''' % (ticks - cx_min * 60))
    kq_cursor.execute('''select content from event where time > %s ''' % (ticks - CX_MIN * 60))
    values = kq_cursor.fetchall()
    return values, len(values)