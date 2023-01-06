from sensor.entity import artifact_entity,config_entity
from sensor.logger import logging
from sensor.exception import SensorException
import os,sys
from scipy.stats import ks_2samp
from typing import Optional
from sensor import utils
import pandas as pd
from sensor.config import target_column


class DataValidation:

    def __init__(self,data_validation_config:config_entity.DataValidationConfig,
    data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:    
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()
    
        except Exception as e:
            raise SensorException(e, sys)

    def drop_missing_values_columns(self,df:pd.DataFrame, report_key_name:str)-> Optional[pd.DataFrame]:
        '''
        This function will drop the columns having missing vlaues more than threshold

        Params:
        df: Accepts a pandas dataframe
        threshold: percentage criteria to drop a columns
        =================================================
        returns Pandas DataFrame if atleast a single column is available after dropping columns else None
        '''
        try:
            threshold = self.data_validation_config.missing_threshold

            #check missing values in every feature
            null_report = df.isnull().sum()/df.shape[0]

            logging.info(f"select column names containing null values more than {threshold*100}%")
            #select column names which contains null valeus more than threshold
            drop_column_names = null_report[null_report>threshold].index

            logging.info(f"columns to drop:{list(drop_column_names)}")
            # record dropped columns in validation error dictionary
            self.validation_error[report_key_name] = list(drop_column_names)
            df.drop(columns = drop_column_names,inplace = True)

            #return None if no column left in dataframe
            if len(df.columns) == 0:
                return None
            return df
        
        except Exception as e:
            raise SensorException(e, sys)

    def is_reuired_column_exists(self,base_df:pd.DataFrame,current_df:pd.DataFrame, report_key_name:str)->bool:
        try:
            base_columns = base_df.columns
            current_columns = current_df.columns

            missing_columns = []
            for base_column in base_columns:
                if base_column not in current_columns:
                    missing_columns.append(base_column)

            if len(missing_columns) > 0:
                self.validation_error[report_key_name] = missing_columns
                return False

            return True

        except Exception as e:
            raise SensorException(e, sys)
    
    def data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame, report_key_name:str):
        try:
            drift_report = dict()
            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_column in base_columns:
                base_data,current_data = base_df[base_column],current_df[base_column]

                #null hypothesis is that both columns data drawn from same distribution
                response = ks_2samp(base_data,current_data)

                if response.pvalue > 0.05:
                    #null hypothesis accepted
                    drift_report[base_column] = {"pvalue":float(response.pvalue),"same distribution":True}
                else:
                    #null hypothesis rejected
                    drift_report[base_column] = {"pvalue":float(response.pvalue),"same distribution":False}

            self.validation_error[report_key_name] = drift_report

        except Exception as e:
            raise SensorException(e, sys)

    def initiate_data_validation(self,)->artifact_entity.DataValidationArtifact:
        try:
            logging.info(f"reading base dataframe")
            base_df = pd.read_csv(self.data_validation_config.base_file_path,na_values="na")

            logging.info(f"drop null values columns from base dataframe")
            #drop missing values columns from base_df 
            base_df = self.drop_missing_values_columns(df = base_df,report_key_name="missing_values_within_base_dataset")

            logging.info(f"reading train dataframe")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            
            logging.info(f"reading test dataframe")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            logging.info(f"drop null values columns from training dataframe")
            #drop missing values columns from train_df
            train_df = self.drop_missing_values_columns(df = train_df,report_key_name="missing_values_within_train_dataset")
            
            logging.info(f"drop null values columns from training dataframe")
            #drop missing values columns from train_df
            test_df = self.drop_missing_values_columns(df = test_df,report_key_name="missing_values_within_test_dataset")

            #converting datatype of all numerical columns to float
            exclude_columns = [target_column]
            base_df = utils.convert_column_float(df = base_df, exclude_columns = exclude_columns)
            train_df = utils.convert_column_float(df = train_df, exclude_columns = exclude_columns)
            test_df = utils.convert_column_float(df = test_df, exclude_columns = exclude_columns)

            logging.info(f"is all required columns present in training dataframe")
            train_df_columns_status = self.is_reuired_column_exists(base_df = base_df, current_df = train_df,report_key_name = "missing_columns_within_train_dataset")
            
            logging.info(f"is all required columns present in test dataframe")
            test_df_columns_status = self.is_reuired_column_exists(base_df = base_df, current_df = test_df,report_key_name = "missing_columns_within_test_dataset")

            if train_df_columns_status:
                logging.info(f"As all columns are available in training dataframe hence detecting data drift")
                self.data_drift(base_df = base_df, current_df = train_df, report_key_name="data_drift_within_train_dataset")
            
            if test_df_columns_status:
                logging.info(f"As all columns are available in test dataframe hence detecting data drift")
                self.data_drift(base_df = base_df, current_df = test_df, report_key_name="data_drift_within_test_dataset")
               
            #write the report
            logging.info(f"writing report in yaml file")
            utils.write_yaml_file(file_path = self.data_validation_config.report_file_path, data = self.validation_error)

            data_validation_artifact = artifact_entity.DataValidationArtifact(
                report_file_path = self.data_validation_config.report_file_path)
            
            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact

        except Exception as e:
            raise SensorException(e, sys)