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
    """Aggregates the best data for each galaxy based on the priority list.

    Takes in a dataframe returns a dataframe with only the best galaxy data 
        for each galaxy in this order:

            List of priority:
            1. Chandra | XMM & HST
            2. Chandra | XMM & SDSS | SAO-DSS
            3. RASS & HST
            4. RASS & SDSS | SAO-DSS
    
    Args:
        data: The DataFrame containing galaxy data

    Returns:
        A pandas DataFrame with only one value per galaxy based on priority list
    """
    
    #A list of all the individual galaxy names. 
    galaxy_names = data.Name.unique().tolist()

    #The DataFrame that will contain the reduced data
    reduced_data = pd.DataFrame()
    
    #Loops through each galaxy name and pulls out the best data for each
    for name in galaxy_names:

        #Sets a variable named galaxy_df to the row that has the 
        #current galaxy name and an x-ray Source that is CHandra or XMM and 
        #an OP Source that equals HST
        #1. Chandra | XMM & HST
        galaxy_df = data[(data['Name'] == name) 
            & ((data['x-ray Source'] == 'Chandra') 
            | (data['x-ray Source'] == 'XMM')) & (data['Op Source'] == 'HST')]
        
        #If there is not a row that contains the current galaxy name,
        #an x-ray Source that is Chandra or XMMM and an Op Source that is HST
        #Then set glaxy_df equal to a row that has an x-ray source of 
        #Chandra of XMM and an Op Source of SDSS or SAO-DSS
        #2. Chandra | XMM & SDSS | SAO-DSS
        if galaxy_df.shape[0] == 0:
            galaxy_df = data[(data['Name'] == name) 
                & ((data['x-ray Source'] == 'Chandra') 
                | (data['x-ray Source'] == 'XMM')) 
                & ((data['Op Source'] == 'SDSS') 
                | (data['Op Source'] == 'SAO-DSS'))]

            #If there is not a row that contains the current galaxy name,
            #an x-ray Source that is Chandra or XMMM and an Op Source that is 
            #SDSS or SAO-DSS, then set glaxy_df equal to a row that 
            #has an x-ray source of Rass and an Op Source of HST
            #3. RASS & HST
            if galaxy_df.shape[0] == 0:
                galaxy_df = data[(data['Name'] == name) 
                    & (data['x-ray Source'] == 'RASS') 
                    & (data['Op Source'] == 'HST')]

                #If there is not a row that contains the current galaxy name,
                #an x-ray Source that is RAAA and an Op Source that is 
                #SDSS or SAO-DSS, then set glaxy_df equal to a row that 
                #has an x-ray source of Rass and an Op Source of SDSS or SAO-SDSS
                #4. RASS & SDSS | SAO-DSS
                if galaxy_df.shape[0] == 0:
                    galaxy_df = data[(data['Name'] == name) 
                        & ((data['x-ray Source'] == 'RASS') 
                        | (data['x-ray Source'] == 'SDSS')) 
                        & ((data['Op Source'] == 'SDSS') 
                        | (data['Op Source'] == 'SAO-DSS'))]

        #Checks to see if galaxy_df has one row and then adds that row to 
        #reduced_data. If it has more or less than one row, print error message
        #and do not add anything to reduced_data.
        try:
            num_of_rows = galaxy_df.shape[0]

            assert (num_of_rows ==  1)

        except AssertionError as error:

            if num_of_rows < 1:
                print ('{} doesn\'t have any rows that fit the'\
                ' parameters given by the priority list.'.format(name))

            elif galaxy_df.shape[0] > 1:
                print ('{} has {} rows that are \'best\'. Check your csv'\
                    ' for double row entries. No rows for this galaxy were '\
                    'added to the DataFrame.').format(name, galaxy_df.shape[0])

        #if the number of rows == 1 then append the row to the reduced_data
        else:
           reduced_data = reduced_data.append(galaxy_df)

    return reduced_data