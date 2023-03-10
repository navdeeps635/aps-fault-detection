from sensor.entity import artifact_entity,config_entity
from sensor.logger import logging
from sensor.exception import SensorException
import os,sys
from typing import Optional
from sensor import utils
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from imblearn.combine import SMOTETomek
from sensor.config import target_column
from sklearn.preprocessing import LabelEncoder,RobustScaler

class DataTransformation:
    
    def __init__(self,data_transformation_config:config_entity.DataTransformationConfig,
    data_ingestion_artifact:config_entity.DataIngestionConfig):

        try:
            logging.info(f"{'>>'*20} Data Transformation {'<<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        
        except Exception as e:
                raise SensorException(e, sys)
    
    @classmethod
    def get_data_transformer_object(cls):
        try:
            simple_imputer = SimpleImputer(strategy = "mean", fill_value = 0)
            robust_scaler = RobustScaler()

            steps = [("Imputer",simple_imputer),("RobustScaler",robust_scaler)]
            pipeline = Pipeline(steps)
            
            return pipeline

        except Exception as e:
            raise SensorException(e, sys)
        
    def initiate_data_transformation(self,)->artifact_entity.DataTransformationArtifact:
        try:
            #read train datafile and test datafile
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            #select input features for train and test dataframe
            input_feature_train_df = train_df.drop(columns = target_column)
            input_feature_test_df = test_df.drop(columns = target_column)

            #select target features for train and test dataframe
            target_feature_train_df = train_df[target_column]
            target_feature_test_df = test_df[target_column]

            #categorical features encoding using LabelEncoder
            label_encoder = LabelEncoder()
            label_encoder.fit(target_feature_train_df)

            #transformation on target column
            target_feature_train_arr = label_encoder.transform(target_feature_train_df)
            target_feature_test_arr = label_encoder.transform(target_feature_test_df)
            
            #transformation pipeline
            transformation_pipeline = DataTransformation.get_data_transformer_object()
            transformation_pipeline.fit(input_feature_train_df)
            
            #transformation on input features
            input_feature_train_arr = transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_arr = transformation_pipeline.transform(input_feature_test_df)

            #handle class imbalance using SMOTETomek
            smt = SMOTETomek(random_state = 42)
            logging.info(f"Before resampling in training set, Input:{input_feature_train_arr.shape} and Target:{input_feature_train_arr.shape}")
            input_feature_train_arr,target_feature_train_arr = smt.fit_resample(input_feature_train_arr,target_feature_train_arr)
            logging.info(f"After resampling in training set, Input:{input_feature_train_arr.shape} and Target:{input_feature_train_arr.shape}")
            
            logging.info(f"Before resampling in test set, Input:{input_feature_test_arr.shape} and Target:{input_feature_test_arr.shape}")
            input_feature_test_arr,target_feature_test_arr = smt.fit_resample(input_feature_test_arr,target_feature_test_arr)
            logging.info(f"After resampling in test set, Input:{input_feature_test_arr.shape} and Target:{input_feature_test_arr.shape}")
            
            #concat train and test array to save into single file.
            train_arr = np.c_[input_feature_train_arr,target_feature_train_arr]
            test_arr = np.c_[input_feature_test_arr,target_feature_test_arr]
            
            #save numpy array
            utils.save_numpy_array_data(file_path = self.data_transformation_config.transformed_train_path, array = train_arr)
            utils.save_numpy_array_data(file_path = self.data_transformation_config.transformed_test_path, array = test_arr)

            utils.save_object(file_path = self.data_transformation_config.transform_object_path, obj = transformation_pipeline)

            utils.save_object(file_path = self.data_transformation_config.target_encoder_path, obj = label_encoder)

            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                            transform_object_path = self.data_transformation_config.transform_object_path,
                            transformed_train_path = self.data_transformation_config.transformed_train_path,
                            transformed_test_path = self.data_transformation_config.transformed_test_path,
                            target_encoder_path = self.data_transformation_config.target_encoder_path)

            logging.info(f"Data transformation object: {data_transformation_artifact}")

            return data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)