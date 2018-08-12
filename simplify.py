import pandas as pd
import numpy as np

"""
List of priority:
1. Chandra | XMM & HST
2. Chandra | XMM & SDSS | SAO-DSS
3. RASS & HST
4. RASS & SDSS | SAO-DSS
"""
def simplify_csv(csv):
    data = pd.read_csv(csv)
    del data['Unnamed: 0']
    data = __reduce(data)
    data = data.sort_values(['Name'])
    
    return data
    
def simplify_df(data):
    data = __reduce(data)
    data = data.sort_values(['Name'])
    
    return data

def __reduce(data):
    galaxy_names = data.Name.unique().tolist()
    reduced_data = pd.DataFrame()
    
    for name in galaxy_names:

        #1. Chandra | XMM & HST
        galaxy_df = data[(data['Name'] == name) 
            & ((data['x-ray Source'] == 'Chandra') 
            | (data['x-ray Source'] == 'XMM')) & (data['Op Source'] == 'HST')]
        
        #2. Chandra | XMM & SDSS | SAO-DSS
        if galaxy_df.shape[0] == 0:
            galaxy_df = data[(data['Name'] == name) 
                & ((data['x-ray Source'] == 'Chandra') 
                | (data['x-ray Source'] == 'XMM')) 
                & ((data['Op Source'] == 'SDSS') 
                | (data['Op Source'] == 'SAO-DSS'))]

            #3. RASS & HST
            if galaxy_df.shape[0] == 0:
                galaxy_df = data[(data['Name'] == name) 
                    & (data['x-ray Source'] == 'RASS') 
                    & (data['Op Source'] == 'HST')]

                #4. RASS & SDSS | SAO-DSS
                if galaxy_df.shape[0] == 0:
                    galaxy_df = data[(data['Name'] == name) 
                        & ((data['x-ray Source'] == 'RASS') 
                        | (data['x-ray Source'] == 'SDSS')) 
                        & ((data['Op Source'] == 'SDSS') 
                        | (data['Op Source'] == 'SAO-DSS'))]

        if galaxy_df.shape[0] > 0:
            reduced_data = reduced_data.append(galaxy_df)
        else:
            print 'oh no {} doesn\'t have any useable data'.format(name)

    return reduced_data