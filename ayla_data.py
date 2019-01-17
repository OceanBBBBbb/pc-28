'''
    怎么去分析这个数据才是最核心的，产生一个怎么的预判结果?
'''

import DB_lucky

def deal_data():
    results = DB_lucky.get_rec(300)
    # 遍历结果
    array_full = [0,0,0,0,0,0,0,0,0,0]
    for row in results: # 这里有100个这样的一组数,每个数都是0-9之间
        # 这里代码可以抽一下
        first_n = int(row[2])
        array_full[first_n]= array_full[first_n]+1
        second_n = int(row[3])
        array_full[second_n] = array_full[second_n] + 1
        thrid_n = int(row[4])
        array_full[thrid_n] = array_full[thrid_n] + 1
    print(array_full) # 这就是每个数出现的次数，下标是数，值是次数，看来100期样本太小了
    return array_full

avg_times= 100# 理论上的平均值 86*3/10
def forecast():
    array_full = deal_data() #拿到数据
    may_num = []
    may_i=0
    array_full_i=0
    for value in array_full:
        if(value<=avg_times*0.618):
            may_num.insert(may_i,array_full_i)
            may_i+=1
        array_full_i+=1
    print("本期可能的数字：")
    print(may_num)
    return may_num

# 最后得出一个结论
def get_conslu():
    may_num = forecast()
    if(len(may_num)==0):
        print("没有预测结论")
    else:
        may_sum=0
        if (len(may_num) <= 3):
            for may in may_num:
                may_sum += may
            print("预计结果大于：" + str(may_sum)) #这个也不准，可能都是最小的那位数呢。
        else: # 大于3位数，就要组合求和了,可以重复的从数列里随机取一个数，一共取三次，求和。列举所有的可能
            print("暂时还没想好")

if __name__ == '__main__':
    # get_conslu()
    print(DB_lucky.get_cash())