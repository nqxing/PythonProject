import threadpool
import time
# 多线程  将两个列表放进一个方法 方法接受2个变量
def hello(m, n):
    """"""
    # print("m = %s, n = %s, o = %s" % (m, n, o))
    # print(m)
    # print(n)
    print('%s:%s' % (m, n))
    time.sleep(2)

#
# if __name__ == '__main__':
#     # 方法1
#     lst_vars_1 = ['1', '11', '111','1111']
#     lst_vars_2 = ['2', '2', '222','2222']
#     # lst_vars_1 = ['1', '2', '3']
#     # lst_vars_2 = ['4', '5', '6']
#     func_var = [(lst_vars_1, None), (lst_vars_2, None)]
#     # 方法2
#     # dict_vars_1 = {'m': '1', 'n': '2', 'o': '3'}
#     # dict_vars_2 = {'m': '4', 'n': '5', 'o': '6'}
#     # func_var = [(None, dict_vars_1), (None, dict_vars_2)]
#
#     pool = threadpool.ThreadPool(2)
#     requests = threadpool.makeRequests(hello, func_var)
#     [pool.putRequest(req) for req in requests]
#     pool.wait()
name_list = ['kebi','maoxian','xiaoniao','xingye']
name_list1 = ['kebi1','maoxian1','xiaoniao1','xingye1']
# for i in range(0,len(name_list1)):
#     nam = name_list[i]
#     name = name_list1[i]
#     # hello(nam,name)
# data = [([(nam for nam in name_list, name for name in name_list1)], None)]
data = [((nam, name), None) for (nam, name) in zip(name_list,name_list1)]  # (index,i)也可以写成[index,i]

pool = threadpool.ThreadPool(4)
requests = threadpool.makeRequests(hello, data)
[pool.putRequest(req) for req in requests]
pool.wait()