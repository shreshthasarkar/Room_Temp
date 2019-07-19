#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'Room_Temp'))
	print(os.getcwd())
except:
	pass

#%%
# Importing Relevant Libraries
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import pylab
import collections
import pymongo
import psycopg2
import paho.mqtt.client as mqtt
import seaborn as sns
from IPython import display
from pandas import datetime
from datetime import timedelta
from pymongo import MongoClient
from scipy import stats

import plotly.graph_objects as go
import plotly as py

py.offline.init_notebook_mode(connected=True)


#%%
# Set up MongoDB Client
client_mqtt = mqtt.Client()

# Set up NodeMCU Client
client_mongo = MongoClient('192.168.1.5')
temp_database = client_mongo['temp_collect']
data_1=temp_database['Temperature_1']
data_2=temp_database['Temperature_2']


#%%
#Time : 2pm - 3pm , AC Temperature : 26, Date : 18/7/19
date_time=[]
tmp_1=[]
tmp_2=[]
tmp_3=[]
avg=[]
#specifying every n'th minute
time=3
#counter
c=time
for obj in data_1.find():
    time_h=(obj['Date-Time'][11:])
    
    #if("15:" in time_h or "15:0" in time_h):
    if("16:" in time_h):
        if(c==time):
            date_time.append(datetime.strptime(obj['Date-Time'],'%m/%d/%Y %H:%M'))
            tmp_1.append(float(obj['tmp_1']))
            tmp_2.append(float(obj['tmp_2']))
            tmp_3.append(float(obj['tmp_3']))
            avg.append((float(obj['tmp_1'])+float(obj['tmp_2'])+float(obj['tmp_3']))/3)
            c=0
        c=c+1

d = {'Temp_1':tmp_1,'Temp_2':tmp_2,'Temp_3':tmp_3,'Avg':avg}
data=pd.DataFrame(d)
d_2 = {'Time':date_time,'Temp_1':tmp_1,'Temp_2':tmp_2,'Temp_3':tmp_3,'Avg':avg}
data_time=pd.DataFrame(d_2)
data_time=data_time.set_index('Time')
sns.lineplot(data=data, palette="tab10", linewidth=2.5)


#%%
data_time.head()


#%%



