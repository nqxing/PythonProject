import sqlite3
conn = sqlite3.connect("yxlm.db")
#创建一个游标 curson
cursor = conn.cursor()
# sql = """ CREATE TABLE eleme_xh(
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    mobile           varchar(100) ,
#    interface            varchar(100) ,
#    sign        varchar(100),
#    sid         varchar(100),
#    qq        varchar(100),
#    sid_getTime        varchar(100),
#    sms_url        varchar(100),
#    is_fiveTimes        varchar(100)
# ); """

sql = """ CREATE TABLE pf_link(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   pf_name           varchar(100) ,
   pf_link            varchar(300)
); """


# sql = """
# INSERT INTO eleme_xh (mobile,interface,sign,sid,qq,sid_getTime,sms_url,is_fiveTimes) VALUES (\'17157721545\', \'BB43A693597FA9BF752804BA860FB05C\', \'064228e9201fd5600f2de7c6392d686a\', \'b0TC1wqFqGJXtQABAasGlfzzy9Uu9gtoPlvA\', \'2799352045\',\'2019-04-21 12:05:11\' ,\'https://www.pdflibr.com/SMSContent/42\',\'已达5次\');
# """
#
# sql = """
# INSERT INTO eleme_lucky (mobile,interface,sign,sid) VALUES (\'15160654911\', \'oEGLvjuHrBqcAmeDwyKqelBp-gw0\', \'24d0edf3b0ad82c914153407758f3380\', \'9z1zS9MV1tCDoRZYEvgSgP5QW7eggeluNWLA\' );
# """
# sql = "UPDATE eleme_jk SET sms_url = 'Texas1111' WHERE mobile = '17128240034'"
# sql = "select mobile from eleme_xh"
# cursor.execute(sql)
# values = cursor.fetchall()
#
# print(str(values))
# conn.commit()

# cursor.execute('''select * from eleme_lucky WHERE id = 3 ''')
# values = cursor.fetchall()
# print(values)

cursor.execute(sql)
conn.commit()