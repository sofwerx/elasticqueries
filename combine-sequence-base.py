

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
#columncount = 5

#annoyingColumns = [datetimename ,'_index', '_source.time' , '_source.timestamp']
#person = False

# Import Libraries
import pandas as pd
from summarizeDataFrame import summarizeDataset
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import sys
import numpy as np
import math

# baseline = pd.read_csv("time_taken2.csv")
#
#baseline['date'] = '2018-04-03'
#
# # baseline['Front Motion Sent'] = pd.to_datetime(baseline['Front Motion Sent']).dt.time
# # baseline['Motion Sensor 2 Received'] = pd.to_datetime(baseline['Motion Sensor 2 Received']).dt.time
# # print(baseline.dtypes)

# baseline['starttime'] = pd.to_datetime(baseline['date'] + ' ' + baseline['Front Motion Sent (Sequence Start)'])
# baseline['endtime'] = pd.to_datetime(baseline['date'] + ' ' + baseline['Lock Received'])
#
# # baseline = baseline.dropna()
# # starttime = baseline.loc[:,'Front Motion Sent'].values
# # endtime = baseline.loc[:,'Motion Sensor 2 Received'].values
# # print(starttime)#
# # print(baseline.head())
# # Need to inlcude for Pots
# #get_ipython().magic(u'matplotlib inline')



# import Data
df = pd.read_csv(datafile)
df11 = pd.read_csv(datafile2)
df31 = pd.read_csv(datafile3)
df41 = pd.read_csv(datafile4)

# make datetime to datetime format
df[datetimename] = pd.to_datetime(df[datetimename])
#df11[datetimename2] = pd.to_datetime(df11[datetimename2])
df11[datetimename2]=pd.to_datetime(df11['_source.DeviceTime'] , unit='ms') - pd.Timedelta(hours=4)
df31[datetimename3] = pd.to_datetime(df31[datetimename3])
df31[datetimename4] = pd.to_datetime(df31[datetimename4])

#print(df11.head())
df11.to_csv("subper.csv", index=False)

# Filter Data
starttime = '2018-04-12 16:03'
endtime = '2018-04-12 17:44'

# Change data to datetime format
df = df[(df[datetimename] > starttime) & (df[datetimename] <= endtime)]
df11 = df11[(df11[datetimename2] > starttime) & (df11[datetimename2] <= endtime)]
df31 = df31[(df31[datetimename3] > starttime) & (df31[datetimename3] <= endtime)]
df41 = df41[(df41[datetimename4] > starttime) & (df41[datetimename4] <= endtime)]

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
ap.sort_values(by=[datetimename],inplace = True)
#ap[datetimename] = pd.to_datetime(ap[datetimename]).values.astype('<M8[m]')
#ap = ap.drop(datetimename , axis=1)

#print(ap)
#df11[]

#print(df1.head())
ap['transactionID'] = ""


list = []

count = 0
row = 0
for x in ap['sequence']:

    if x == 'nannannannannanFrontLock1nannannannannannannannanUnlockednannannan Manny Kinwebhook':
        count = count + 1


    #df1.loc[row, 'ID'] = count
    #df1.ix[row, 'ID'] = count
    ap.iloc[row, ap.columns.get_loc('transactionID')] = count
    #df1['ID'] == count
    #print(row,count)
    row = row + 1


#print(df1.head())

ap2=ap[['transactionID','sequence']]
#df3=df2.loc[df2['transactionID']] != 0
ap3=ap2[(ap2['transactionID'] > 0)]

# =ap3['transactionID'].value_counts()
#ap3['Data4'] = ap3['transactionID'].groupby(ap3['transactionID']).count()
#ap3['counts'] = ap3.groupby(['sequence','transactionID'])["sequence"].count()
# ap4=ap3.groupby(['sequence','transactionID'])["sequence"].count().reset_index(name="count")
#g = ap3.groupby('transactionID')['transactionID'].value_counts().reset_index(name='t')
#ap3['count'] = ap3.groupby('transactionID')['sequence'].transform('count')
ap4=ap3[ap3.duplicated('transactionID',keep=False)]
ap4=ap4[['transactionID','sequence']]



#
# ap4.sort_values(by=['transactionID'],inplace = True)
#df3=df2.loc[:, df2.loc['transactionID']  >= 0 ]
#print(df3)
ap4.to_csv("test3.csv", index=False)
ap.to_csv("subper.csv", index=False)

print(df41)


'''



#df2=df1['sequence'].astype(str)


# Make data set divisible by wanted column
# rowCount = (int(len(df2.index)))
# columnCountRows = math.floor(rowCount/ columncount)
# newRowCount = math.floor(rowCount/ columncount) * columncount
#df2 = df2[:newRowCount].astype(str)
#df3 =pd.DataFrame(np.reshape(df2.values,(columnCountRows,5)))
#df2=df1['sequence']
df1['nextone']=df1['sequence'].shift(-1)
df1['nextwo']=df1['sequence'].shift(-2)
df1['nextthree']=df1['sequence'].shift(-3)
df1['nextfour']=df1['sequence'].shift(-4)
df1['nextfive']=df1['sequence'].shift(-5)
df1['nextsix']=df1['sequence'].shift(-6)
df1['nextseven']=df1['sequence'].shift(-7)
df1['nexteight']=df1['sequence'].shift(-8)
#df1.drop(df1.tail(9).index,inplace=True)
df2 = df1.reset_index()


df3 = df2[df2.columns[-9:]]
# print(df3)
df3=df3.loc[df3['sequence'] == 'nannannannannanFrontLock1nannannannanUnlockednannannan Manny Kinwebhook']

df3.reset_index( inplace=True)
#print(df3.head())
#df3.to_csv("sequence-ifttt2.csv", index=False)
df3['transactionID'] = df3.index
#print(df3.head())
df4 = pd.melt(df3, id_vars=['transactionID'], value_vars=['sequence', 'nextone' , 'nextwo' , 'nextthree' , 'nextfour' , 'nextfive' , 'nextsix' , 'nextseven' , 'nexteight'])
#print(df3)
#print(df4.head())

df11 = df3.head(1)
df12 = pd.melt(df11, id_vars=['transactionID'], value_vars=['sequence', 'nextone' , 'nextwo' , 'nextthree' , 'nextfour' , 'nextfive' , 'nextsix' , 'nextseven' , 'nexteight'])

del df4['variable']
del df12['variable']
#print(df11)
df4.to_csv("test3.csv", index=False)
#df4.to_csv("sequence-ifttt.csv", index=False)
df12.to_csv("test.csv", index=False)




#new.df <- data.frame(s1 = head(df$regions,-1), s2 = tail(df$regions,-1))


#print(df3.head())


# print (pd.DataFrame(df2.values.reshape(-1, 5),
#                     columns=['Name','School','Music','Mentor1','Mentor2']))
#print(np.reshape(df2.values,(len(df2.index),5)))

#print(df2)

# df[datetimename]= df[datetimename].apply(lambda x:x.strfdatetime( '%Y-%d-%m %H:%M:%S'))

# Initialize Scenario count Variable
# df['desired_output'] = ""
#
# # Start and endtime data
# # array = ["2018-03-26 18:16:16.658","2018-03-20 18:16:17.696","2018-03-20 18:16:18.707"]
# # array2 = ["2018-04-02 18:16:19.732","2018-03-20 18:16:19.732","2018-03-20 18:16:19.732"]
# array = baseline['starttime'].values
# array2 = baseline['endtime'].values
#
# # Create unique identifier for scenario aggregation
# count = 1
#
# for i, x in zip(array, array2):
#     df['desired_output'] = np.where(
#         np.logical_and(df[datetimename] >= pd.to_datetime(i), df[datetimename] <= pd.to_datetime(x)), count,
#         df['desired_output'])
#
#     count = count + 1
#
# # print(df)
#
# # Filter Data for no unique and high unique
# if person == True:
#
#     df2 = df.loc[:, df.apply(pd.Series.nunique) != int(len(df.index))]
#
# else:
#
#     do = df.loc[:, 'desired_output']
#     df1 = df.loc[:, df.apply(pd.Series.nunique) != 1]
#
#     df2 = df1.loc[:, df1.apply(pd.Series.nunique) != int(len(df1.index))]
#
#     if 'desired_output' not in df2.columns:
#         df2 = pd.concat([do, df2], axis=1)

# # Remove Unessary Columns
# if all([item in df2.columns for item in annoyingColumns]):
#
#     df3 = df2.drop(annoyingColumns, axis=1)
#
# else:
#
#     df3 = df2
#
#
#
# # Get names of column aggregation
# names = list(df3)
# if 'desired_output' in names:
#
#     names.remove('desired_output')
#
# else:
#
#     print("Scenario Not in Dataset")
#     print(list(df2))
#     sys.exit()
#
# # print(df3)
#
# # Create Dummy Variable for Dataset
# df5 = pd.get_dummies(df3, columns=names)
# df5.index = df[datetimename]
#
# # df6=df5.resample("5T").count()
#
# df6 = df5.groupby(['desired_output'], as_index=False)[list(df5)].nunique()

# df2  = df1.groupby(['_source.device']).agg({'_source.action': [ min , max ,'first', 'nunique','count']})



# summarizeDataset(df3)


# print(list(df4))
# print(type(names1))
# print(df5.head())
# # print(baseline)
# # print(array2[2])
# df6.to_csv("features-ifttt.csv", index=False)
#
#
#
# print(baseline[['starttime', 'endtime']])
#
# # print(df5.groupby(['desired_output'])[list(df5)].count())
# #
# print(df6)
# # print(list(df))


'''