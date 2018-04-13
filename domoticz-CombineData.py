###################################################################################
########################## Data Prepartion - Event Generation #####################
###################################################################################

# Notes
# Each Data Source will be dowloaded independently




# Initialize Variables

# Datafile Name
datafile = "domoticz.csv"
datetimename = 'datetime'

annoyingColumns = ['_index', '_source.Time']
person = False

# Import Libraries
import pandas as pd
from summarizeDataFrame import summarizeDataset
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import sys
import numpy as np

baseline = pd.read_csv("time_taken2.csv")

baseline['date'] = '2018-04-03'

# baseline['Front Motion Sent'] = pd.to_datetime(baseline['Front Motion Sent']).dt.time
# baseline['Motion Sensor 2 Received'] = pd.to_datetime(baseline['Motion Sensor 2 Received']).dt.time
# print(baseline.dtypes)
baseline['starttime'] = pd.to_datetime(baseline['date'] + ' ' + baseline['Front Motion Sent (Sequence Start)'])
baseline['endtime'] = pd.to_datetime(baseline['date'] + ' ' + baseline['Lock Received'])

# baseline = baseline.dropna()
# starttime = baseline.loc[:,'Front Motion Sent'].values
# endtime = baseline.loc[:,'Motion Sensor 2 Received'].values


# print(starttime)

# print(baseline.head())




# Need to inlcude for Pots
#get_ipython().magic(u'matplotlib inline')


# import Data
df = pd.read_csv(datafile)

# make datetime to datetime format
df[datetimename] = pd.to_datetime(df[datetimename]).values.astype('<M8[s]')
# df[datetimename]= df[datetimename].apply(lambda x:x.strfdatetime( '%Y-%d-%m %H:%M:%S'))

# Initialize Scenario count Variable
df['desired_output'] = ""

# Start and endtime data
# array = ["2018-03-26 18:16:16.658","2018-03-20 18:16:17.696","2018-03-20 18:16:18.707"]
# array2 = ["2018-04-02 18:16:19.732","2018-03-20 18:16:19.732","2018-03-20 18:16:19.732"]
array = baseline['starttime'].values
array2 = baseline['endtime'].values

# Create unique identifier for scenario aggregation
count = 1

for i, x in zip(array, array2):
    df['desired_output'] = np.where(
        np.logical_and(df[datetimename] >= pd.to_datetime(i), df[datetimename] <= pd.to_datetime(x)), count,
        df['desired_output'])

    count = count + 1

# print(df)

# Filter Data for no unique and high unique
if person == True:

    df2 = df.loc[:, df.apply(pd.Series.nunique) != int(len(df.index))]

else:

    do = df.loc[:, 'desired_output']
    df1 = df.loc[:, df.apply(pd.Series.nunique) != 1]

    df2 = df1.loc[:, df1.apply(pd.Series.nunique) != int(len(df1.index))]

    if 'desired_output' not in df2.columns:
        df2 = pd.concat([do, df2], axis=1)

# Remove Unessary Columns
if all([item in df2.columns for item in annoyingColumns]):

    df3 = df2.drop(annoyingColumns, axis=1)

else:

    df3 = df2



# Get names of column aggregation
names = list(df3)
if 'desired_output' in names:

    names.remove('desired_output')

else:

    print("Scenario Not in Dataset")
    print(list(df2))
    sys.exit()

# print(df3)

# Create Dummy Variable for Dataset
df5 = pd.get_dummies(df3, columns=names)
df5.index = df[datetimename]

# df6=df5.resample("5T").count()

df6 = df5.groupby(['desired_output'], as_index=False)[list(df5)].nunique()

# df2  = df1.groupby(['_source.device']).agg({'_source.action': [ min , max ,'first', 'nunique','count']})



# summarizeDataset(df3)


# print(list(df4))
# print(type(names1))
# print(df5.head())
# print(baseline)
# print(array2[2])
df6.to_csv("features-domoticz.csv", index=False)



print(baseline[['starttime', 'endtime']])

# print(df5.groupby(['desired_output'])[list(df5)].count())
#
print(df6)
# print(list(df))


