
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


   
##### Handle for Large Data  #####    

# Row Count
rowCount = len(df.index)


# if dataset is larger than 100 thousands 
# records sample 100 thousand
if rowCount > 10000:

   df1 = df.sample(n=10000)
else:    

   df1 = df

del df    

##################################


#Remove attributes with zero variance. Assumming  Datetime is not Unique
df2 = df1.loc[:,df1.apply(pd.Series.nunique) != 1]

del df1

# Seperate Numerical and Categorical Variable to View data
numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
numerical = df2.select_dtypes(numerics)

categorical = df2.drop(list(df2.select_dtypes(numerics)), axis=1)

#df_num = df.apply(lambda x: x.cat.codes)


print("Categorical Variables" + "\n")
print(categorical.head())
print("\n"+ "Numerical Variables"  + "\n")
print(numerical.head())





# Data Understanding

# View Summary of dataset
print("\n"  +  "Categorical Data Summary")
summarizeDataset(categorical)
print("Numerical Data Summary")
summarizeDataset(numerical)


# View Scatterplot
scatter_matrix(df2, figsize=[15, 15], marker='x', diagonal='hist')
plt.show()

#

numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
newdf = df2.select_dtypes(numerics)
del df2







dat = newdf



## perform PCA

n = len(dat.columns)

pca = PCA(n_components=n)
# defaults number of PCs to number of columns in imported data (ie number of
# features), but can be set to any integer less than or equal to that value

pca.fit(dat)



print("PCA-Explained Variance" + "\n" )
print(pca.explained_variance_ratio_)

## project data into PC space

# 0,1 denote PC1 and PC2; change values for other PCs
xvector = pca.components_[0]  # see 'prcomp(my_data)$rotation' in R
yvector = pca.components_[1]

xs = pca.transform(dat)[:, 0]  # see 'prcomp(my_data)$x' in R
ys = pca.transform(dat)[:, 1]

## visualize projections

## Note: scale values for arrows and text are a bit inelegant as of now,
##       so feel free to play around with them

for i in range(len(xvector)):
   # arrows project features (ie columns from csv) as vectors onto PC axes
   plt.arrow(0, 0, xvector[i] * max(xs), yvector[i] * max(ys),
             color='r', width=0.01, head_width=0.0025)
   plt.text(xvector[i] * max(xs) * 1.2, yvector[i] * max(ys) * 1.2,
            list(dat.columns.values)[i], color='r')

for i in range(len(xs)):
   # circles project documents (ie rows from csv) as points onto PC axes
   plt.plot(xs[i], ys[i], 'bo')
 
plt.figure(figsize=(15,15))
plt.show()
print("done")


#newdf.to_csv("pca1.csv" , index=False)






# In[ ]:




# In[ ]:



