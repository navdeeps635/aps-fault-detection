import pymongo
import pandas as pd
import json

# Provide the mongodb localhost url to connect python to mongodb.
client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

#database and collection name
database_name = "aps"
collection_name = "sensor"

#data file path
data_file_path = '/config/workspace/aps_failure_training_set1.csv'

if __name__ == '__main__':
    df = pd.read_csv(data_file_path)
    print(df.shape)

    #convert dataframe to JSON so that we can dump these records in mongodb
    df.reset_index(drop=True,inplace=True)

    json_records = list(json.loads(df.T.to_json()).values())
    #print(json_records[0])

    #insert converted json records to mongodb
    client[database_name][collection_name].insert_many(json_records)