import subprocess
import json
from pandas.io.json import json_normalize
from summarizeDataFrame import summarizeDataset
from datetime import datetime

import pandas as pd
from time import strptime
import search_elastic as se
import numpy as np

# Initialized variables

elasticdatetimecolumn = '_source.timestamp'

# JSON Query
#
# body = {
#     "query": {
#         "range" : {
#             "timestamp" : {
#                 "gte" : "now-2d",
#                  "lt" :  "now/d"
#             }
#         }
#     }
# }



body ={
    "query": {
        "match" : {
            "module" : 9
        }
    }
}

#body = {"query": {"range": {"timestamp": {"gte": "now-1d/d", "lt": "now/d"}}}}


# Elasticsearch instance
data = se.search_elastic('gammarf' , body )


# Store data to dataframe
d = pd.DataFrame(json_normalize(data))



#Number of transactions

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

#del d

#
df['DateTime'] =pd.to_datetime(df[elasticdatetimecolumn])
df.sort_values(by=['DateTime'],inplace = True)

df["Date"] = df['DateTime'].dt.date
df["Hour"] = df['DateTime'].dt.hour
df["Minute"] = df['DateTime'].dt.minute

df = df[['Date','Hour','Minute','_source.module']]
df = df.groupby(['Date','Hour','Minute']).size().rename('count').reset_index()

df['ServerTime'] = pd.to_datetime(df["Date"]) + pd.to_timedelta(df["Hour"], unit='h') + pd.to_timedelta(df["Minute"], unit='m')
df.sort_values(by=['ServerTime'],inplace = True)

df['RFStatus'] = np.where(df['count'] < 50 , 'RF','RF-ATTACK')

df.to_csv("gammarfTEST.csv", index=False)

df=df[(df['RFStatus'] == 'RF-ATTACK')]

#df['ServerTime'] = df["Hour"] + ':' + df['Minute']

df = df[['ServerTime' ,'RFStatus','count' ]]

#ap[(ap['freq'] >= 3)]



df.to_csv("gammarf.csv", index=False)


print(df.dtypes)
print('\n',"Total Transactions:",totalT ,'\n')
print("Total Rows:",len(df) ,'\n')
print(df.tail(10))

#print(list(df))
#
#
# #
#
# #df.to_csv("/home/david/Desktop/new.csv" , sep='\t' , index=False)
#
#
