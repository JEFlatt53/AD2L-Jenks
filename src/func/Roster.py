import glob
import pandas as pd
from .MMR import *

def CombineRosters(rostersDir):
    filePaths = glob.glob(rostersDir + '/*.[ct]sv')
    dataframes = []
    for filePath in filePaths:
        try:
            print("Reading file: " + filePath)
            if filePath.endswith('.csv'):
                df = pd.read_csv(filePath)
            elif filePath.endswith('.tsv'):
                df = pd.read_csv(filePath, delimiter='\t')
            df = df.dropna(how='all')
            df = df.drop(columns=['Unnamed: 4', 'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 8'])
            df.columns = ['TeamName', 'PlayerName', 'Rank', 'DotaBuff', 'Stratz', 'TeamWeight']
            df = df.ffill()
            df['MMR'] = df['Rank'].apply(GetMMR)
            dataframes.append(df)
        except:
            print("Skipping file: " + filePath)
    return pd.concat(dataframes, ignore_index=True)

def Teams(df):
    dfs = [data[1] for data in df.groupby('TeamName')]
    return dfs



