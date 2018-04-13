import subprocess
import json
from pandas.io.json import json_normalize
from summarizeDataFrame import summarizeDataset
from datetime import datetime , timedelta

import pandas as pd
from time import strptime
import search_elastic as se

# Initialized variables

elasticdatetimecolumn = '_source.timestamp'

# JSON Query
#
# body = {
#     "query": {
#         "range" : {
#             "timestamp" : {
#                 "gte" : "now-4d",
#                  "lt" :  "now/d"
#             }
#         }
#     }
# }

#body = {"query": {"range": {"timestamp": {"gte": "now-1d/d", "lt": "now/d"}}}}


# Elasticsearch instance
data = se.search_elastic('ifttt*' )


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

# Convert to EST
df['DateTime'] = df['DateTime'] - timedelta(hours=4)


print('\n',"Total Transactions:",totalT ,'\n')
print("Total Rows:",len(df) ,'\n')

print(df.tail())
#summarizeDataset(df)


df.to_csv("ifttt.csv", index=False)
#
#
# #
#
# #df.to_csv("/home/david/Desktop/new.csv" , sep='\t' , index=False)
#
#
