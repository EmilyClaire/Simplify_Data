"""Reduces the data in the csv to only one row per galaxy
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
            or None if there was a problem.
    """
    
    #Checks to see if the data_in variable is a str or pandas DataFrame.
    #If data_in is not a str or DataFrame, prints a message 
    #and returns a None value
    try:
        assert (isinstance(data_in, str) or isinstance(data_in, pd.DataFrame))

    except AssertionError as error:
        print "Invalid Type: Only accepts csv path/filenames as a str " \
            "or DataFrames"
        return None

    #checks to see if data_in is a str. If it is a str but cannot be read by
    #pd.read_csv, then the IOError is caught and a message is printed and
    #the function returns a None value.
    #if the file is a str and can be read by pd.read_csv, then the csv file
    #is read into a DataFrame
    if isinstance(data_in, str):
        
        try:
            data = pd.read_csv(data_in)
         
        except IOError as error:
            print "I/O error: {}".format(error)
            print "Could not simplify file: Make sure the the path and filename"\
            " are correct"
            return None
 
    #Because the try block at the top of this function checks to make sure that
    #the data_in variable is either a DataFrame or a str, we can use an else
    #statement to handle the DataFrame actions.
    #In this case, the data_in variable is copied to the data variable.
    else:
        data = pd.DataFrame(data_in)


    #check to see if there is a random column in there named 'Unnamed: 0'
    #if so, delete the column
    if 'Unnamed: 0' in data.columns.values.tolist():
        del data['Unnamed: 0']

    #Call the function that actually reduces the data and set it equal to data
    data = __reduce(data)
    
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