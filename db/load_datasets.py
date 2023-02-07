from datawarehouse.models import Dataset, Database
import quandl
import numpy as np
import datetime

quandl.ApiConfig.api_key = 'H2wsJr5sJBEowokpwG4T'


def save_datasets_to_db():
    dbs = [db for db in quandl.Database.all() if not db['premium']]
    for db in dbs:
        if not Database.objects.filter(database_code=db.database_code).exists():
            Database.objects.create(name=db.name, database_code=db.database_code, description=db.description)
        db0 = Database.objects.get(database_code=db.database_code)
        for dataset in list(db.datasets()):
            if not Dataset.objects.filter(source='quandl', database_code=db0, dataset_code=dataset.dataset_code).exists():
                Dataset.objects.create(source='quandl', database_code_id=dataset.database_code,
                                       dataset_code=dataset.dataset_code, name=dataset._raw_data['name'][:255], description=dataset._raw_data['description'][:1022],
                                       frequency=dataset._raw_data['frequency'])



def list_datasets():
    return Dataset.objects.all()


def get_data(dataset, start_date, end_date):
    return quandl.get(dataset, start_date=start_date, end_date=end_date)
