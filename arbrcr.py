# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 01:04:44 2015

@author: Moon
"""

import os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

start_time = time.time()

date_array = {}
merge_base = ['code' , 'name', 'market']#這個放要合併基準
# date_array[0] 就是最靠新資料的DataFrame
# 如果要改計算天數，就改下面這個range的數字, 22是月
cal_date = 10 #在這邊設定天數

file_path = 'C:/1save/jpStock/rawPython/' #檔案路徑的代號，這邊放歷史資料
history_list = []
for name in os.listdir(file_path):
    history_list.append(name)


def sortDataFromNew (source_list, index):
    #source_list,是目標的list,第二個是存放目標的diction名字,第三個是裡面的code
    history_number = int(len(source_list)) - 1   
    code = str(index)
    def_diction = {}
    for i in range(history_number):
        def_diction[code + str(i)] = source_list[history_number]
        history_number = history_number - 1
    return def_diction
    
string = sortDataFromNew (history_list, 'd')
#print (string['d0'])

#string = sorted(string.values())
#pre_array =pd.read_csv(file_path + string['d0'], encoding = 'utf-8')

#print (pre_array[:5])
def makeDailyPriceArray(file_path, date):
      
    #程式的一開始 一定要放
    #import pandas as pd 
    #不然會執行不了
    
    #而且前面要先用 sortDateFromNew 先處理過歷史資料
    # !!! You must import pandas as pd first
    #file_path => 放的是歷史資料
    #date      => 只要輸入數字, 0 表示最新的資料; 1 表示 前1天; 2表示前 2天
    
    
    file_path = str(file_path)
    #date = str(date)
    #array_name = str(array_name)
    
    sort_index = 'd' + str(date)
    
    csv_columns = ['code','market','name','industry','open','high','low','close','volumn','daily_money']
    
    pre_array =pd.read_csv(file_path + string[sort_index], skiprows = 1,encoding = 'utf-8')
    pre_array.columns = csv_columns    
    pre_array['volumn'] = pre_array['volumn'].astype(int) #先把vol換成int
       
    pre_array = pre_array[pre_array.volumn != 0] #然後在array裡面去掉vol = 0
    #pre_array.index = pre_array['code'] #把index設定成code之後才好合併
    pre_array['open'] = pre_array['open'].astype(float)
    pre_array['high'] = pre_array['high'].astype(float)
    pre_array['low'] = pre_array['low'].astype(float)
    pre_array['close'] = pre_array['close'].astype(float)
    pre_array = pre_array.drop(['industry', 'volumn', 'daily_money'], axis = 1) 
    pre_array = pre_array.rename(columns = {'open' : 'd' + str(date) + '_open','high' : 'd' + str(date) +  '_high', 'low': 'd' + str(date) +  '_low', 'close' : 'd' + str(date) +  '_close'})
       
    #array_index = sort_index + '_array'
    #print (array_index)
    return pre_array
    #print (array_name)
#date_array[0] = makeDailyPriceArray(file_path, 0)


for i in range (int(cal_date)-1):
    date_array[i] = makeDailyPriceArray(file_path, i) 
    #這個i不能把他當成string
    if i == 0:
        pass
    elif i == 1:
        merge_array = pd.merge (date_array[0], date_array[1], on = merge_base)
    else :
        merge_array = pd.merge (merge_array, date_array[i], on = merge_base)

"""
#以下是ar
"""

for i in range(int(cal_date)-1):
    #merge_array_h = merge_array.loc[:,'code']
    #merge_array_l = merge_array_h
    merge_array['ar_d' + str(i) + '_diff_h'] = merge_array['d' + str(i) + '_high'] - merge_array['d' + str(i) + '_open']
    #merge_array_h['d' + str(i) + '_diff_h'] = merge_array['d' + str(i) + '_diff_h']    
    
for i in range(int(cal_date)-1): 
    merge_array['ar_d' + str(i) + '_diff_l'] = merge_array['d' + str(i) + '_open'] - merge_array['d' + str(i) + '_low']



group_col_h = []
group_col_l = []

for i in range(int(cal_date)-1):
    h_index = 'd' + str(i) + '_diff_h'
    group_col_h.append(h_index)
    l_index = 'd' + str(i) + '_diff_l'
    group_col_l.append(h_index)

"""
merge_array['ar_h'] = merge_array[['d1_diff_h', 'd2_diff_h', 'd3_diff_h', 'd4_diff_h', 'd5_diff_h', 'd6_diff_h', 'd7_diff_h', 'd8_diff_h']].sum(axis = 1)
merge_array['ar_l'] = merge_array[['d1_diff_l', 'd2_diff_l', 'd3_diff_l', 'd4_diff_l', 'd5_diff_l', 'd6_diff_l', 'd7_diff_l', 'd8_diff_l']].sum(axis = 1)
merge_array['ar_h'] = merge_array['ar_h'].astype(float)
merge_array['ar_l'] = merge_array['ar_l'].astype(float)
merge_array = merge_array[merge_array['ar_l'] != 0]
merge_array['ar'] = merge_array['ar_h'] /merge_array['ar_l']
only1_array = merge_array[merge_array['market'].str.contains("1")]

merge_array = merge_array.sort(columns = 'ar', axis = 0, ascending=[False])
only1_array = only1_array.sort(columns = 'ar', axis = 0, ascending=[False])
"""
merge_array = merge_array.set_index('code') #之後要改
#only1_array = only1_array.set_index('code') #之後要改

#df1.sort(['a', 'b'], ascending=[True, False])
#data2 = data.set_index('a')
"""
merge_array_h = merge_array.loc [:,'code', 'd0_diff_h':'d' + str(int(cal_date)-2) + '_diff_h']
merge_array_h['ar_aum_h'] = merge_array_h.sum(axis = 1)

merge_array_l = merge_array.loc [:,'code', 'd0_diff_l': 'd' + str(int(cal_date)-2) + '_diff_l']
merge_array_l['ar_aum_l'] = merge_array_l.sum(axis = 1)

merge_array['ar_aum_h'] = merge_array_h['ar_aum_h']
merge_array['ar_aum_l'] = merge_array_l['ar_aum_l']
merge_array['ar'] = merge_array['ar_aum_h'] / merge_array['ar_aum_l']
"""

ar_array_h = merge_array.ix[:, 'ar_d0_diff_h':'ar_d' + str(int(cal_date)-2) + '_diff_h']
ar_array_h['ar_aum_h'] = ar_array_h.sum(axis=1)

ar_array_l = merge_array.ix[:, 'ar_d0_diff_l':'ar_d' + str(int(cal_date)-2) + '_diff_l']
ar_array_l['ar_aum_l'] = ar_array_l.sum(axis=1)

merge_array['ar_aum_h'] = ar_array_h['ar_aum_h'].astype(float)
merge_array['ar_aum_l'] = ar_array_l['ar_aum_l'].astype(float)
merge_array = merge_array[merge_array['ar_aum_l'] != 0]
merge_array['ar'] = merge_array['ar_aum_h'] /merge_array['ar_aum_l']

"""
# 以下是br
"""

for i in range(int(cal_date) - 2):
    merge_array['br_d' + str(i) + '_diff_h'] = merge_array['d' + str(i) + '_high'] - merge_array['d' + str(int(i) + 1) + '_close']

for i in range(int(cal_date) - 2):
    merge_array['br_d' + str(i) + '_diff_l'] = merge_array['d' + str(int(i) + 1) + '_close'] - merge_array['d' + str(i) + '_low']

br_array_h = merge_array.ix[:, 'br_d0_diff_h':'br_d' + str(int(cal_date)-3) + '_diff_h']
br_array_h['br_aum_h'] = ar_array_h.sum(axis=1)

br_array_l = merge_array.ix[:, 'br_d0_diff_l':'br_d' + str(int(cal_date)-3) + '_diff_l']
br_array_l['br_aum_l'] = br_array_l.sum(axis=1)

merge_array['br_aum_h'] = br_array_h['br_aum_h'].astype(float)
merge_array['br_aum_l'] = br_array_l['br_aum_l'].astype(float)
merge_array = merge_array[merge_array['br_aum_l'] != 0]
merge_array['br'] = merge_array['br_aum_h'] /merge_array['br_aum_l']

"""
#以下是cr
"""
for i in range(int(cal_date) - 2):
    merge_array['cr_d' + str(i) + 'base'] = (merge_array['d' + str(int(i) + 1) + '_close'] + merge_array['d' + str(int(i) + 1) + '_high'] + merge_array['d' + str(int(i) + 1) + '_low']) / 3

for i in range(int(cal_date) - 2):
    merge_array['cr_d' + str(i) + '_diff_h'] = merge_array['d' + str(i) + '_high'] - merge_array['cr_d' + str(i) + 'base']

for i in range(int(cal_date) - 2):
    merge_array['cr_d' + str(i) + '_diff_l'] = merge_array['cr_d' + str(i) + 'base'] - merge_array['d' + str(i) + '_low']

cr_array_h = merge_array.ix[:, 'cr_d0_diff_h':'cr_d' + str(int(cal_date)-3) + '_diff_h']
cr_array_h['cr_aum_h'] = ar_array_h.sum(axis=1)

cr_array_l = merge_array.ix[:, 'cr_d0_diff_l':'cr_d' + str(int(cal_date)-3) + '_diff_l']
cr_array_l['cr_aum_l'] = cr_array_l.sum(axis=1)

merge_array['cr_aum_h'] = cr_array_h['cr_aum_h'].astype(float)
merge_array['cr_aum_l'] = cr_array_l['cr_aum_l'].astype(float)
merge_array = merge_array[merge_array['cr_aum_l'] != 0]
merge_array['cr'] = merge_array['cr_aum_h'] /merge_array['cr_aum_l']


only1_array = merge_array[merge_array['market'].str.contains("1")]

merge_array = merge_array.sort(columns = 'ar', axis = 0, ascending=[False])
only1_array = only1_array.sort(columns = 'ar', axis = 0, ascending=[False])
#result_array = merge_array.loc [:50, 'code', 'market', 'name', 'ar']
#only1_array = merge_array[merge_array['market'].str.contains("1")]
#print (result_array[10:])




print("Run time --- %s seconds ---" % (time.time() - start_time))
