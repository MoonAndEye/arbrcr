# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 11:41:07 2015

"""

import os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

pd.set_option('display.mpl_style', 'default')
pd.set_option('display.width' , 5000)
pd.set_option('display.max_columns', 60)

writein_path = 'C:/1save/jpStock/arbrcr/arbrcr.csv'

pre_array =pd.read_csv(writein_path, index_col = 0, encoding = 'utf-8')

pre_array['ar'].plot()
