import subprocess
import json, os, time
from pandas.io.json import json_normalize
from summarizeDataFrame import summarizeDataset
from datetime import datetime

import numpy as np
import pandas as pd
from time import strptime
import search_elastic as se

# Initialized variables

elasticdatetimecolumn = '_id'

total_row_count = 0
data_save_time = 0

def fetch_data():
    global total_row_count, data_save_time
    data = se.search_elastic('domoticz*')

    # Store data to dataframe
    d = pd.DataFrame(json_normalize(data))

    # Number of transactions
    totalT=int(len(d))

    if totalT == 1:
        df = json_normalize(d.ix[0, 'hits.hits'])
    else:


    # Append hits to dataframe
        df = pd.DataFrame([])

        for x in range( 0 , totalT - 1) :
            ed=json_normalize(d.ix[x, 'hits.hits'] )
            df = df.append(ed)

    # Garbarge collect dataframe
    del d

    # Filter to date time values only
    df=df[df[elasticdatetimecolumn].str.contains("GMT")]


    # # Find Datetime and make dateime sortable
    df2=df[elasticdatetimecolumn]
    df3 = df2.str.split(' ', expand=True)
    df4 = df3.ix[:, 1]
    df3.ix[:, 1]=df3.ix[:, 1].apply(lambda x: strptime(x,'%b').tm_mon)

    df3['date'] = pd.to_datetime(df3.ix[:, 1].astype(int).astype(str)+'/'+df3.ix[:, 2].astype(int).astype(str)+'/'+df3.ix[:, 3].astype(int).astype(str) , format = '%m/%d/%Y').dt.date.astype(str)
    df3['time'] = df3.ix[:, 4].astype(str)
    df['datetime'] =  pd.to_datetime(df3['date'] + ' ' + df3['time'])
    df.sort_values(by=['datetime'],inplace = True)

    #Garbage collect dataframe
    del df2, df3, df4

    # Get Device name
    df['devicename']=df['_source.message'].str.split(' ', expand=True).ix[:, 0]

    # #summarizeDataset(df2)
    # View Meta Data
    print('\n',"Total Transactions:",totalT ,'\n')
    total_row_count += df.shape[0]
    print("Total Rows:",total_row_count ,'\n')

    ## Save data
    df.to_csv("domoticz.csv", index=False)
    colnames = df.columns.values.tolist()

    start_time_datasave = time.time()

    # save column names
    cols2save = os.path.join("data/raw","domoticz_df_colnames.npy")
    np.save(cols2save, colnames)

    file2save = os.path.join("data/raw","domoticz_df_" + str(total_row_count) + ".npy")
    np.save(file2save, df)

    data_save_time = data_save_time + (time.time() - start_time_datasave) / 60
    # print("Time taken to save data (mins): ", data_save_time)


    #

    # df.to_csv("domoticz.csv" , index=False)
start_time = time.time()
while total_row_count <= 100000:
    print("Current row count: ", total_row_count)
    fetch_data()

print("Total Time taken in (mins): ", (time.time() - start_time) / 60)
print("Time to save data in (mins): ", data_save_time)