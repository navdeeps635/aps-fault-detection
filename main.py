from sensor.pipeline.training_pipeline import start_training_pipeline
from sensor.pipeline.batch_prediction import start_batch_prediction
from sensor.exception import SensorException
import os,sys

file_path = "/config/workspace/aps_failure_training_set1.csv"

if __name__ =="__main__":
    try:
        output_file = start_batch_prediction(input_file_path = file_path)
    except Exception as e:
            raise SensorException(e, sys)
