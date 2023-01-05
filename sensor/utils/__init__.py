import pandas as pd
from sensor.config import mongo_client
from sensor.logger import logging
from sensor.exception import SensorException
import os,sys

def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    '''
    Description: This function coonvert database collection into dataframe.

    Params:
    database_name:database name
    collection_name: collecttion name
    ======================================
    returns: pandas dataframe of a collection.
    '''

    try:
        logging.info(f"reading data from database: {database_name} and collection: {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        
        logging.info(f"found columns: {df.columns}")
        if "_id" in df.columns:

            logging.info(f"dropping column: _id")
            df.drop(columns = ["_id"],inplace = True)
        
        return df

    except Exception as e:
        raise SensorException(e,sys)