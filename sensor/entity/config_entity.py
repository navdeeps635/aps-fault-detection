import os,sys
from datetime import datetime
from sensor.exception import SensorException
from sensor.logger import logging

file_name = "sensor.csv"
train_file_name = "train.csv"
test_file_name = "test.csv"

class TrainingPipelineConfig:

    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(),"artifact",f"{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}")
        except Exception  as e:
            raise SensorException(e,sys)

class DataIngestionConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig,):
        
        try:
            self.database_name = "aps"
            self.collection_name = "sensor"
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir,"data_ingestion")
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_store",file_name)
            self.train_file_path = os.path.join(self.data_ingestion_dir,"Dataset",train_file_name)
            self.test_file_path = os.path.join(self.data_ingestion_dir,"Dataset",test_file_name)
            self.test_size = 0.2
        except Exception as e:
            raise SensorException(e, sys)

    def to_dict(self,)->dict:
        try:
            return self.__dict__
        except Exception as e:
            raise SensorException(e, sys)


class DataValidationConfig:...
class DataTransformationConfig:...
class ModelTrainerConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...