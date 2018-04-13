import subprocess
import json, os, time
from pandas.io.json import json_normalize
from summarizeDataFrame import summarizeDataset
from datetime import datetime
import numpy as np
import pandas as pd
import search_elastic as se

# Initialized variables

elasticdatetimecolumn = '_source.@timestamp'


total_row_count = 0

def fetch_data():
    global total_row_count

    # Query ElasticSearch with Scroll
    data = se.search_elastic('auditbeat-6.2.2-2018.02.27')


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

    #Garbage collect dataframe
    del d

    # Convert timestamp to date time to sort by datetime
    df['DateTime'] =pd.to_datetime(df[elasticdatetimecolumn])
    df.sort_values(by=['DateTime'],inplace = True)

    print('\n',"Total Transactions:",totalT ,'\n')
    total_row_count += df.shape[0]
    print("Total Rows:",total_row_count ,'\n')

    ## Save data
    colnames = df.columns.values.tolist()

    start_time_datasave = time.time()
    # save column names
    cols2save = os.path.join("data/raw","auditbeat_df_colnames.npy")
    np.save(cols2save, colnames)

    file2save = os.path.join("data/raw","auditbeat_df_" + str(total_row_count) + ".npy")
    np.save(file2save, df)

    print("Time taken to save data (mins): ", (time.time() - start_time_datasave) / 60)

    # #df.to_csv("/home/david/Desktop/new.csv" , sep='\t' , index=False)
    #
    #

start_time = time.time()
while total_row_count <= 1000000:
    fetch_data()

print("Total Time taken in (mins): ", (time.time() - start_time) / 60)
