"""
Contains functions that return a DataFrame with only the best galaxy data in it.

Attributes:

Todo:
    * Find out if should throw exceptions or have the code just blow up
    * Find out what license type is used for the project
    * Find out how to add an author to this header
"""

import pandas as pd
import numpy as np

def simplify(data_in):

    """Aggregates the best data for each galaxy based on the priority list.

    Takes in a csv file or data frame and returns a dataframe with only
        the best galaxy data for each galaxy in this order:

            List of priority:
            1. Chandra | XMM & HST
            2. Chandra | XMM & SDSS | SAO-DSS
            3. RASS & HST
            4. RASS & SDSS | SAO-DSS
    
    Args:
        data_in: The csv file pathname or the DataFrame containing galaxy data

    Returns:
        A pandas DataFrame with only one value per galaxy based on priority list
    """

    if isinstance(data_in, str):
        data = pd.read_csv(data_in)
        del data['Unnamed: 0']
    
    elif isinstance(data_in, pd.DataFrame):
        data = data_in

    else:
        print "Invalid Type: Only accepts strings and DataFrames"
        return

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