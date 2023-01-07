import os,sys
from sensor.entity import config_entity 
from glob import glob
from typing import Optional 


class ModelResolver:

    def __init__(self,model_registry:str = "saved_models",
    transformer_dir_name:str = "transformer",
    target_encoder_dir_name:str = "targer_encoder",
    model_dir_name:str = "model"):

        self.model_registry = model_registry
        os.makedirs(self.model_registry,exist_ok=True)
        self.transformer_dir_name = transformer_dir_name
        self.target_encoder_dir_name = target_encoder_dir_name
        self.model_dir_name = model_dir_name

    def get_latest_dir_path(self)->Optional[str]:
        '''This function will give path of earlier saved model'''
        try:
            dir_names = os.listdir(self.model_registry)
            if len(dir_names) == 0:
                return None
            dir_names = list(map(int,dir_names))
            latest_dir_name = max(dir_names)
            return os.path.join(self.model_registry,f"{latest_dir_name}")

        except Exception as e:
            raise SensorException(e, sys)
 
    def get_latest_model_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                return Exception(f"Model is not available")
            return os.path.join(latest_dir, self.model_dir_name,config_entity.model_file_name)

        except Exception as e:
            raise SensorException(e, sys)

    def get_latest_transfomer_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Transformer is not available")
            return os.path.join(latest_dir, self.transformer_dir_name,config_entity.transformer_object_file_name)

        except Exception as e:
            raise SensorException(e, sys)
    
    def get_latest_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Target encoder is not available")
            return os.path.join(latest_dir, self.target_encoder_dir_name,config_entity.target_encoder_object_file_name)

        except Exception as e:
            raise SensorException(e, sys)

    def get_latest_save_dir_path(self)->str:
        '''This function will create path for latest model to save'''
        try:
            latest_dir = self.get_latest_dir_path()
            
            if latest_dir == None:
                return os.path.join(self.model_registry,f"{0}")

            latest_dir_num = int(os.path.basename(self.get_latest_dir_path()))

            return os.path.join(self.model_registry,f"{latest_dir_name+1}")

        except Exception as e:
            raise SensorException(e, sys)
    
    def get_latest_save_model_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir, self.model_dir_name,config_entity.model_file_name)

        except Exception as e:
            raise SensorException(e, sys)

    def get_latest_save_transfomer_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir, self.transformer_dir_name,config_entity.transformer_object_file_name)

        except Exception as e:
            raise SensorException(e, sys)
    
    def get_latest_save_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir, self.target_encoder_dir_name,config_entity.target_encoder_object_file_name)

        except Exception as e:
            raise SensorException(e, sys)

class Predictor:

    def __init__(self,model_resolver:ModelResolver):
        self.model_resolver = model_resolver

    def get_latest_dir_path(self):
        try:
            dir_names = os.listdir(self.model_registry)
            dir_names = map(int,dir_names)
            latest_dir_name = max(dir_names)
            return os.path.join(self.model_registry,f"{latest_dir_name}")

        except Exception as e:
            raise SensorException(e, sys)