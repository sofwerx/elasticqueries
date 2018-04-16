
###########################################################################################
#################################### Functions ############################################
###########################################################################################

# Function summarizes your pandas dataframe dataset. There needs to be header names in dataframe
def summarizeDataset(df):

    import pandas as pd

    columnNames = df.columns.values
    count = 1
    print( '\n'+ "Dataframe Attribute Names and Formats")
    print("--------------------------------------")
    print( '\n' + str(df.dtypes) + '\n')

    print("Dataframe Summary Statistics" )
    print("--------------------------------------" + '\n')

    for columnName in columnNames:

        count = count
        print("(" + str(count) + ")" + '\n')
        print("Attribute Name:" +columnName + '\n')
        #print(columnName + '\n')
        print("Attribute Summary Statistics:" + '\n')
        print(str(df[str(columnName)].describe()) + '\n')
        print("Unique Values:" + '\n')
        print(str(df[str(columnName)].unique()) + '\n' + '\n')
        count = count + 1


############################################################################################
#################################### Data Analysis #########################################
############################################################################################


