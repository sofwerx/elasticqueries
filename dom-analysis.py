
# coding: utf-8

# In[24]:


   
   # Initialize Variables
# Datafile Name
datafile = "domoticz.csv"



# Data Preperation

# Notes
# Assuming Dateime is not unique
# Assuming not many nonzero variance columns
# If datarows are larger than 100,000 will only sample 100,000


# Import Libraries
import pandas as pd
from summarizeDataFrame import summarizeDataset
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
import sys


# Need to inlcude for Pots
get_ipython().magic(u'matplotlib inline')

# import Data
df = pd.read_csv(datafile)

# Add Datetime format
df['datetime'] = pd.to_datetime(df['datetime'])

#df1 = df[(df['datetime'] > '2018-03-01') & (df['datetime'] < '2013-03-30')]
df1 = df[(df['datetime'] > '2018-03-26')]



# #Remove attributes with zero variance. Assumming  Datetime is not Unique
# df2 = df1.loc[:,df1.apply(pd.Series.nunique) != 1]

# del df1

# # Seperate Numerical and Categorical Variable to View data
# numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
# numerical = df2.select_dtypes(numerics)

# categorical = df2.drop(list(df2.select_dtypes(numerics)), axis=1)

# #df_num = df.apply(lambda x: x.cat.codes)


# print("Categorical Variables" + "\n")
# print(categorical.head())
# print("\n"+ "Numerical Variables"  + "\n")
# print(numerical.head())





# Data Understanding

# View Summary of dataset
print("\n"  +  "Categorical Data Summary")
summarizeDataset(categorical)
print("Numerical Data Summary")
summarizeDataset(numerical)

display(df2)

#df2.to_csv("test.csv" , index=False)


# print(df1.dtypes)
# print(df1.head())
# print("Total Rows:",len(df1) ,'\n')


# In[ ]:



