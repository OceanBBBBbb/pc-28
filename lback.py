'''
    回测已有的数据，看胜率几何
'''
from Include import DB_lucky
from Include import data_by_trend
from Include import high_odds

#回测56期内热门数
def lback_56_hot():
    results = DB_lucky.get_all(820)# 从id大于值的数据开始来回测
    init_re = list(results[:56]) # 这是最初的数据

    for i,row in enumerate(results):  # 从旧到新
        if(i>55):
            trade_nums = data_by_trend.anly_data(init_re) #本轮下的单
            real_re = row[5] #本轮的结果
            forecast = 0 #0不正确，1正确
            if(real_re in trade_nums):#预判正确
                forecast=1
            DB_lucky.update_fore(forecast,row[0])
            init_re.append(list(row)) #末尾追加最新一期的数据
            del init_re[0]


lback_56_hot()
# high_odds.sleeping_l(400)