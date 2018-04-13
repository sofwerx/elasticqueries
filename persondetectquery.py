


import subprocess
import json
from pandas.io.json import json_normalize
from summarizeDataFrame import summarizeDataset
from datetime import datetime

import pandas as pd
from time import strptime
import search_elastic as se

# Initialized variables

elasticdatetimecolumn = '_source.DeviceTime'

#print(json.dumps(data, indent=4))


data = se.search_elastic('persondetect')

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

# Convert timestamp to date time to sort by datetime
df['datetime'] =  pd.to_datetime(df[elasticdatetimecolumn] , unit='ms')
df.sort_values(by=['datetime'],inplace = True,ascending=False)


# Convert to EST
df['datetime'] = df['datetime'].apply(lambda x: x.tz_localize('UTC').tz_convert('US/Eastern'))

# df['EST'] = (df.datetime.dt.tz_localize('UTC')
#                         .tz_convert('US/Eastern')
#                         .strftime("%H:%M:%S"))


df.to_csv("persondetect.csv", index=False)

# View Meta Data
print('\n',"Total Transactions:",totalT ,'\n')
print("Total Rows:",len(df) ,'\n')
print(df.head())


# #summarizeDataset(df2)


#


#df.to_csv("/home/david/Desktop/new.csv" , sep='\t' , index=False)







#
#     df = json_normalize(item['hits']['hits'])

#print(json_normalize(item['hits']['hits']))
# new=json_normalize(data['responses'])
# data1 = pd.read_json(string,typ='index')
#res['hits']['hits']
#df = pd.concat(map(pd.DataFrame.from_dict, data), axis=1)['hits'].T
#print(new.head())
