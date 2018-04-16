

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



datetimename = 'DateTime'
datetimename2 = 'datetime'
datetimename3 = '_source.timestamp'
datetimename4 = '_source.timestamp'


# Import Libraries
import pandas as pd
from summarizeDataFrame import summarizeDataset
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from datetime import datetime , timedelta
from pandas.plotting import scatter_matrix
import sys
import numpy as np
import math



# import Data
df = pd.read_csv(datafile)
df11 = pd.read_csv(datafile2)
df31 = pd.read_csv(datafile3)
df41 = pd.read_csv(datafile4)

# make datetime to datetime format
df[datetimename] = pd.to_datetime(df[datetimename])
#df11[datetimename2] = pd.to_datetime(df11[datetimename2])
df11[datetimename2]=pd.to_datetime(df11['_source.DeviceTime'] , unit='ms') - pd.Timedelta(hours=4)
df31[datetimename3] = pd.to_datetime(df31[datetimename3]) - pd.Timedelta(hours=4)
df31[datetimename4] = pd.to_datetime(df31[datetimename4]) - pd.Timedelta(hours=4)

#print(df11.head())
df11.to_csv("subper.csv", index=False)

# Filter Data




#starttime = '2018-04-13 16:54'
#endtime = '2018-04-13 17:27'

now = datetime.now()
now_minus_10 = str(now - timedelta(minutes = 5))

print(now_minus_10)
# Change data to datetime format
df = df[(df[datetimename] > now_minus_10) ]
df11 = df11[(df11[datetimename2] > now_minus_10) ]
df31 = df31[(df31[datetimename3] > now_minus_10) ]
df41 = df41[(df41[datetimename4] > now_minus_10) ]

#print(df11.head())


# Remove unnessary columns
df1 = df.drop(["_id" ,"_index" , '_score' , '_source.time' ,'_source.timestamp' , datetimename], axis=1)
df12 = df11.drop(["_id" ,"_index" , '_score' , '_source.Count','_source.DeviceID' , '_source.DeviceID' , '_source.DeviceTime','_source.LocationID', '_type' , '_source.Class' ], axis=1)
#print(df1.head())
#
# Unique iftt events
df1=df1.astype(str)
df1['sequence'] = df1.apply(''.join, axis=1)
df1 = pd.concat([df1, df[datetimename]], axis=1)

# Add Variable to destiguish data sources
df12['sequence'] = 'person'
df31['sequence'] = 'Unknown-Webcam'
df41['sequence'] = 'Unknown-Device'

# Rename Time Variable for datetime form sources
df12.rename(columns={datetimename2: datetimename}, inplace=True)
df31.rename(columns={datetimename3: datetimename}, inplace=True)
df41.rename(columns={datetimename4: datetimename}, inplace=True)




# Subset interesting datsources
df1 = df1[[datetimename,'sequence']]
df31 = df31[[datetimename, 'sequence']]
df41 = df41[[datetimename, 'sequence']]
ap = df1.append(df12, ignore_index=True)
ap = ap.append(df31, ignore_index=True)
ap = ap.append(df41, ignore_index=True)
ap.sort_values(by=[datetimename],inplace = True)
ap = ap.reset_index(drop=True)
ap['transactionID']= (ap.index / 3 + 1).astype(int)
#print(ap)





ap2=ap[['transactionID','sequence']]

ap2 = ap2[(ap2.sequence == "nannannannannanRoom1LampnannannannanOffnannannannannannannannanwebhook") &
          (ap2.sequence == "nannannannannanPlug1nannannannanActivatednannannannannannannannanwebhook") &
          (ap2.sequence == "nannannannannanRoom1Plug1nannannannanActivatednannannannannannannannanwebhook")
          ]

ap4=ap2
#ap4=ap4[['transactionID','sequence']]




#
# ap4.sort_values(by=['transactionID'],inplace = True)
#df3=df2.loc[:, df2.loc['transactionID']  >= 0 ]
#print(df3)
ap4.to_csv("anomaly.csv", index=False)
ap.to_csv("subper.csv", index=False)

print(ap4)


