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
"""
start_date = 'd'+ str(i) #i 裡面放數字,如果是d0,就是今天,d1就是前一天  
cal_date = 'd'+ str(k) #放的是結束時間,現在不確定要放什麼,可能放數字比較好,舉例來說,從d0算到D20
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
        def_diction[code + str(i)] = source_list[history_number][:-4]
        history_number = history_number - 1
    return def_diction

date_dic = sortDataFromNew (source_pool, 'd')

print("Run time --- %s seconds ---" % (time.time() - start_time))
