from sensor.exception import SensorException
from sensor.logger import logging
from sensor.predictor import ModelResolver
import pandas as pd
import os,sys
from datetime import datetime
from sensor.utils import load_object
import numpy as np

prediction_dir = "prediction"

def start_batch_prediction(input_file_path:str):
    try:
        os.makedirs(prediction_dir,exist_ok=True)
        logging.info(f"creating model resolver object")
        model_resolver = ModelResolver(model_registry="saved_models")

        logging.info(f"Reading input file:{input_file_path}")
        df = pd.read_csv(input_file_path)
        df.replace({"na":np.NAN},inplace=True)

        logging.info(f"loading transformer to transform dataset")
        transformer = load_object(file_path = model_resolver.get_latest_transfomer_path())

        input_feature_names = list(transformer.feature_names_in_)
        input_arr =  transformer.transform(df[input_feature_names])

        logging.info(f"loading model to make predictions")
        model = load_object(file_path = model_resolver.get_latest_model_path())
        prediction = model.predict(input_arr)

        logging.info(f"target encoder to convert predicted column into categorical")
        target_encoder = load_object(file_path = model_resolver.get_latest_target_encoder_path())

        cat_prediction = target_encoder.inverse_transform(prediction)

        df["prediction"] = prediction
        df["cat_prediction"] = cat_prediction

        prediction_file_name = os.path.basename(input_file_path).replace(".csv",f"{'_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}.csv")
        prediction_file_path = os.path.join(prediction_dir,prediction_file_name)
        df.to_csv(prediction_file_path,index = False, header = True)

        return prediction_file_path
    except Exception as e:
        raise SensorException(e,sys)