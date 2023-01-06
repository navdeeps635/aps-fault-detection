import os,sys
from datetime import datetime
from sensor.exception import SensorException
from sensor.logger import logging

file_name = "sensor.csv"
train_file_name = "train.csv"
test_file_name = "test.csv"
transformer_object_file_name = "tranasformer.pkl"
target_encoder_object_file_name = "target_encoder.pkl"
model_file_name = "model.pkl"

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

class DataValidationConfig:
    try:
        def __init__(self,training_pipeline_config:TrainingPipelineConfig):
            self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir,"data_validation")
            self.report_file_path = os.path.join(self.data_validation_dir,"report.yaml")
            self.missing_threshold:float = 0.7
            self.base_file_path = os.path.join("aps_failure_training_set1.csv")

    except Exception as e:
         raise SensorException(e, sys)

class DataTransformationConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_transform_dir = os.path.join(training_pipeline_config.artifact_dir,"data_transformation")
            self.transform_object_path = os.path.join(self.data_transform_dir,"transformer",transformer_object_file_name)
            self.transformed_train_path = os.path.join(self.data_transform_dir,"transformed",train_file_name.replace("csv", "npz"))
            self.transformed_test_path = os.path.join(self.data_transform_dir,"transformed",test_file_name.replace("csv", "npz"))
            self.target_encoder_path = os.path.join(self.data_transform_dir,"target_encoder",target_encoder_object_file_name)
            
        except Exception as e:
            raise SensorException(e, sys)


class ModelTrainerConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir,"model_trainer")
            self.model_path = os.path.join(self.model_trainer_dir , "model",model_file_name)
            self.expected_score = 0.7
            self.overfitting_threshold = 0.1

        except Exception as e:
            raise SensorException(e, sys) 
class ModelEvaluationConfig:...
class ModelPusherConfig:...