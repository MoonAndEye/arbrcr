# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 01:04:44 2015

@author: Moon
"""

import os, random, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict
import time

start_time = time.time()

date_array = {}
merge_base = ['code' , 'name', 'market']#這個放要合併基準
# date_array[0] 就是最靠新資料的DataFrame
# 如果要改計算天數，就改下面這個range的數字, 22是月
date = 5 #在這邊設定天數

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


def makeDailyPriceArray(file_path, date):
    """    
    程式的一開始 一定要放
    import pandas as pd 
    不然會執行不了
    
    而且前面要先用 sortDateFromNew 先處理過歷史資料
    # !!! You must import pandas as pd first
    file_path => 放的是歷史資料
    date      => 只要輸入數字, 0 表示最新的資料; 1 表示 前1天; 2表示前 2天
    """    
    
    file_path = str(file_path)
    date = str(date)
    #array_name = str(array_name)
    
    sort_index = 'd' + str(date)
    
    csv_columns = ['code','market','name','industry','start','high','low','end','volumn','daily_money']
    
    pre_array =pd.read_csv(file_path + string[sort_index], encoding = 'utf-8')
    pre_array.columns = csv_columns    
    pre_array['volumn'] = pre_array['volumn'].astype(int) #先把vol換成int
       
    pre_array = pre_array[pre_array.volumn != 0] #然後在array裡面去掉vol = 0
    #pre_array.index = pre_array['code'] #把index設定成code之後才好合併
    pre_array['start'] = pre_array['start'].astype(float)
    pre_array['high'] = pre_array['high'].astype(float)
    pre_array['low'] = pre_array['low'].astype(float)
    pre_array['end'] = pre_array['end'].astype(float)
    pre_array = pre_array.drop(['industry', 'volumn', 'daily_money'], axis = 1) 
    pre_array = pre_array.rename(columns = {'start' : 'd' + str(date) + '_start','high' : 'd' + str(date) +  '_high', 'low': 'd' + str(date) +  '_low', 'end' : 'd' + str(date) +  '_end'})
       
    #array_index = sort_index + '_array'
    #print (array_index)
    return pre_array
    #print (array_name)


for i in range (date):
    date_array[i] = makeDailyPriceArray(file_path, i) 
    #這個i不能把他當成string
    if i == 0:
        pass
    elif i == 1:
        merge_array = pd.merge (date_array[0], date_array[1], on = merge_base)
    else :
        merge_array = pd.merge (merge_array, date_array[i], on = merge_base)
for i in range(date):
    stop_index = date -1
    merge_array ['d' + str(i) + '_range'] = merge_array['d' + str(i) + '_high'] - merge_array['d' + str(i) + '_end']
    merge_array ['d' + str(i) + '_indicate'] = merge_array['d' + str(i) + '_high'] + merge_array['d' + str(i) + '_end']
    if i != stop_index:
        next_date = i + 1
        merge_array ['d' + str(i) + '_slope'] = (merge_array['d' + str(i) + '_end'] - merge_array['d' + str(next_date) + '_end']) / merge_array ['average']


print("Run time --- %s seconds ---" % (time.time() - start_time))