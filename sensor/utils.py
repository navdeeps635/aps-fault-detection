import pandas as pd
from sensor.config import mongo_client
from sensor.logger import logging
from sensor.exception import SensorException
import os,sys
import yaml
import numpy as np
import dill

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


def write_yaml_file(file_path,data:dict):
    try:
        file_dir = os.path.dirname(file_path)

        os.makedirs(file_dir,exist_ok=True)

        with open(file_path,"w") as file_writer:
            yaml.dump(data,file_writer)

    except Exception as e:
        raise SensorException(e,sys)

def convert_column_float(df:pd.DataFrame,exclude_columns:list)->pd.DataFrame:
    try:
        for column in df.columns:
            if column not in exclude_columns:
                df[column] = df[column].astype('float')
        return df
    
    except Exception as e:
        raise SensorException(e, sys)

def save_object(file_path:str,obj:object)-> None:
    try:
        logging.info(f"Entered the save_object method of Mainutils class")
        os.makedirs(os.path.dirname(file_path),exist_ok = True)

        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
        logging.info(f"Exited the save_object method of Mainutils class")

    except Exception as e:
        raise SensorException(e, sys)

def load_object(file_path:str)-> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exist")
        
        with open(file_path,'rb') as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise SensorException(e, sys)

def save_numpy_array_data(file_path:str,array:np.array):
    """
    save numpy array data to file
    file_path:str location of file to save
    array:np.array data to save
    """
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok = True)

        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    
    except Exception as e:
        raise SensorException(e, sys)

def load_numpy_array_data(file_path:str)-> np.array:
    """
    load numpy array data from file
    file_path:str location of file to load
    array:np.array data to load
    """
    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)

    except Exception as e:
        raise SensorException(e, sys)