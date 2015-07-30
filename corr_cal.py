# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 14:36:39 2015

"""
import os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time


start_time = time.time()

start_date = 'd'+ str(0) #i 裡面放數字,如果是d0,就是今天,d1就是前一天  

cal_date = str(10)  #放的是結束時間,現在不確定要放什麼,可能放數字比較好,舉例來說,從d0算到D20
"""
accu_duration = int(j) #放累加的時間, ar br cr 都有一個累加時間,但最短是5天,不然計算誤差超大
cal_target = '' #放股票代碼前四碼,只放數字
"""
source_path = 'C:/1save/jpStock/rawPython/' #歷史資料的路徑

source_pool = []
for name in os.listdir(source_path):
    source_pool.append(name)

def sortDataFromNew (source_list, index):
    #source_list,是目標的list,第二個是存放目標的diction名字,第三個是裡面的code
    history_number = int(len(source_list)) - 1   
    code = str(index)
    def_diction = {}
    for i in range(history_number):
        def_diction[code + str(i)] = source_list[history_number][:-4] #這是砍掉副檔名的狀態
        history_number = history_number - 1
    return def_diction

date_dic = sortDataFromNew (source_pool, 'd') #這個array只放日期,把後面的副檔名砍掉了

#print (date_dic[start_date])

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

print("Run time --- %s seconds ---" % (time.time() - start_time))
