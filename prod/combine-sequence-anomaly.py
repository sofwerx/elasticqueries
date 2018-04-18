

###################################################################################
########################## Data Prepartion - Event Generation #####################
###################################################################################

# Notes
# Each Data Source will be dowloaded independently




# Initialize Variables

# Datafile Name
datafile = "ifttt.csv"
datafile2 = "persondetect.csv"
datafile3 = "webcam-pcap.csv"
datafile4 = "safehouse-ap-devices.csv"
datafile5 = "gammarf.csv"



datetimename = 'DateTime'
datetimename2 = 'datetime'
datetimename3 = '_source.timestamp'
datetimename4 = '_source.timestamp'
datetimename5 = 'ServerTime'


# Import Libraries
import pandas as pd
from summarizeDataFrame import summarizeDataset
from datetime import datetime , timedelta
from pandas.plotting import scatter_matrix
import sys
import numpy as np
import math
import os



# import Data
df = pd.read_csv(datafile)
df11 = pd.read_csv(datafile2)
df31 = pd.read_csv(datafile3)
df41 = pd.read_csv(datafile4)
df51 = pd.read_csv(datafile5)

# make datetime to datetime format
df[datetimename] = pd.to_datetime(df[datetimename])
#df11[datetimename2] = pd.to_datetime(df11[datetimename2])
df11[datetimename2]=pd.to_datetime(df11['_source.DeviceTime'] , unit='ms') - pd.Timedelta(hours=4)
df31[datetimename3] = pd.to_datetime(df31[datetimename3])
df41[datetimename4] = pd.to_datetime(df41[datetimename4])
df51[datetimename5] = pd.to_datetime(df51[datetimename5])

#print(df11.head())
df11.to_csv("subper.csv", index=False)

# Filter Data




starttime = '2018-04-17 10:00'
endtime = '2018-04-17 11:00'

now = datetime.now()
now_minus_10 = str(now - timedelta(minutes = 5))

print(now_minus_10)
# Change data to datetime format
df = df[(df[datetimename] > now_minus_10) ]
df11 = df11[(df11[datetimename2] > now_minus_10) ]
df31 = df31[(df31[datetimename3] > now_minus_10) ]
df41 = df41[(df41[datetimename4] > now_minus_10) ]
df51 = df51[(df51[datetimename5] > now_minus_10) ]

# print(df.dtypes)
# print(df11.dtypes)
# print(df31.dtypes)
#print(df.dtypes)
#print(df.head())


# Remove unnessary columns
df1 = df.drop(["_id" ,"_index" , '_score' , '_source.time' ,'_source.timestamp' , datetimename], axis=1)
df12 = df11.drop(["_id" ,"_index" , '_score' , '_source.Count','_source.DeviceID' , '_source.DeviceID' , '_source.DeviceTime','_source.LocationID', '_type' , '_source.Class' ], axis=1)
#print(df1.head())
#
# Unique ifttt events
df1=df1.astype(str)
df1['sequence'] = df1.apply(''.join, axis=1)
df1 = pd.concat([df1, df[datetimename]], axis=1)

# Add Variable to destiguish data sources
df12['sequence'] = 'person'
df31['sequence'] = 'Unknown-Webcam'
df41['sequence'] = 'Unknown-Device'
df51['sequence'] = df51['RFStatus']

# Rename Time Variable for datetime form sources
df12.rename(columns={datetimename2: datetimename}, inplace=True)
df31.rename(columns={datetimename3: datetimename}, inplace=True)
df41.rename(columns={datetimename4: datetimename}, inplace=True)
df51.rename(columns={datetimename5: datetimename}, inplace=True)




# Subset interesting datsources
df1 = df1[[datetimename,'sequence']]
df12 = df12[[datetimename,'sequence']]
df31 = df31[[datetimename, 'sequence']]
df41 = df41[[datetimename, 'sequence']]
df51 = df51[[datetimename, 'sequence']]


ap = df1.append(df12, ignore_index=True)
ap = ap.append(df31, ignore_index=True)
ap = ap.append(df41, ignore_index=True)
ap = ap.append(df51, ignore_index=True)

#print(ap.dtypes)
ap.sort_values(by=[datetimename],inplace = True)
ap = ap.reset_index(drop=True)
ap = ap[(ap.sequence != "nannannannannanRoom1LampnannannannanOffnannannannannannannannanwebhook") &
          (ap.sequence != "nannannannannanPlug1nannannannanActivatednannannannannannannannanwebhook") &
          (ap.sequence != "nannannannannanRoom1Plug1nannannannanActivatednannannannannannannannanwebhook")
          ]

#ap['transactionID']= (ap.index / 3 + 1).astype(int)


#print(df1.head())
ap['transactionID'] = ""
ap['count'] = ""


list = []

count = 0
trans = 0
n = 1
row = 0
y = ""
for x in ap['sequence']:


    if x != y:

        count = count + 1
        trans = trans + 1

        if trans > 3:

             trans = 1
             n = n + 1

    ap.iloc[row, ap.columns.get_loc('count')] = count
    ap.iloc[row, ap.columns.get_loc('transactionID')] = n

    row = row + 1
    y = x

#print(ap)
print(ap)

ap['sequence'] = np.where(ap['sequence']=='nannannannannanFrontLock1nannannannannannannannanUnlockednannannanManny Kinwebhook', 'nannannannannanFrontLock1nannannannannannannannanUnlockednannannan Manny Kinwebhook', ap['sequence'])
ap['freq'] = ap.groupby('transactionID')['transactionID'].transform('count')


ap2=ap[(ap['freq'] >= 3)]
#ap2=ap[(ap['transactionID'] == )]

# ap2 = ap2[(ap2.sequence == "nannannannannanRoom1LampnannannannanOffnannannannannannannannanwebhook") &
#           (ap2.sequence == "nannannannannanPlug1nannannannanActivatednannannannannannannannanwebhook") &
#           (ap2.sequence == "nannannannannanRoom1Plug1nannannannanActivatednannannannannannannannanwebhook")
#           ]


ap4=ap2[['transactionID','sequence']]
#ap4=ap4[['transactionID','sequence']]




#
# ap4.sort_values(by=['transactionID'],inplace = True)
#df3=df2.loc[:, df2.loc['transactionID']  >= 0 ]
#print(df3)
ap4.to_csv("anomaly.csv", index=False)
ap.to_csv("subper.csv", index=False)

print(ap)
print(os.getcwd())

