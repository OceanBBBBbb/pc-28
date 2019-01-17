'''
    通过走势数据分析
    http://www.pceggs.com/play/28zs.aspx?id=56
    取这个页面的数据，取56期，获取就是取数据库最新的56期数据
    这个策略就是：买“实际次数”>=“标准次数”的数
'''
from Include import DB_lucky

def get_need_data():
    results = DB_lucky.get_rec(56)  # 先查到最新的56期数据
    return anly_data(results)

def anly_data(results):
    array_trend = [0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 2, 2, 1, 1, 1, 0, 0, 0]  # 结果的预期期数
    array_full_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 28种结果
    for row in results:  # 从新到旧
        num = int(row[5])  # 这个数是几，几号位置+1
        array_full_num[num] = array_full_num[num] + 1
    need_num = []
    for index, cur_num in enumerate(array_full_num):
        if (cur_num >= array_trend[index]):
            need_num.append(index)
    print(need_num)  # 这样就得到了要下单的数据
    return need_num

def get_cash():
    result = DB_lucky.get_cash()
    for cash in result:
        return str(cash[0]).replace(',','')

# True表示输了，Flase表示赢了
def get_if_win():
    result = DB_lucky.get_if_win()
    for win in result:
        re = str(win[0]).replace(',','')
        return '-' in re

# get_need_data()
# print(get_cash())
# print('-' in '-5765')