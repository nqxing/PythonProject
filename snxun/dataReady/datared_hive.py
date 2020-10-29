

for i in range(10):
    txt = "{},zy{},SZ{},这是测试数据这是测试数据这是测试数据{}！\n"
    with open("hive_data(10).txt", "a", encoding='utf-8') as f:
        f.write(txt.format(i+1,i+1,i+1,i+1))