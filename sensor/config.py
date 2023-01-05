import pymongo
import pandas as pd
import json
from dataclasses import dataclass
import os

@dataclass
class EnvironmentVariable:
    
    # Provide the mongodb localhost url to connect python to mongodb.
    mongodb_url:str = os.getenv("mongodb_url")
    
env_variable = EnvironmentVariable()

mongo_client = pymongo.MongoClient(env_variable.mongodb_url)