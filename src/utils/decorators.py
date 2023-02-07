import os
import datetime
import pandas as pd
import re
import datetime
from .formatting import color_cell, add_hyperlinks
from datawarehouse.models import UpdateTime


# decorator that checks if a file with data exists and whether it's recent enough (param refresh rate in seconds).
# refresh rate specifies (in seconds) how often files should be updated
def load_or_save(filename, refresh_rate=60):
    def decorator(func):
        def wraps(*args, **kwargs):
            if filename in os.listdir() and datetime.datetime.now().timestamp() - os.path.getmtime(filename) < refresh_rate:
                print(f'Data loaded from file: {filename}')
                return pd.read_csv(filename, index_col=0)
            else:
                print(f'Getting fresh data and updating file: {filename}')
                data = func(*args, **kwargs)
                df = pd.DataFrame(data)
                df.to_csv(filename, index=False)
                return data
        return wraps
    return decorator




def prep_crypto_display():
    def decorator(func):
        def wraps(*args, **kwargs):
            data = func(*args, **kwargs)
            for col in data.columns:
                if re.search(col, str(['Price', 'Δ', 'vol', 'cap', 'Supply'])):
                    data[col] = data[col].apply(lambda x: format(x, ','))
                    if 'Δ' in col:
                        data[col] = data[col].apply(color_cell)
            data = add_hyperlinks(data)
            if 'Url' in data.columns:
                data.drop('Url', inplace=True, axis=1)
            return data
        return wraps
    return decorator


def load_or_save2(df, dataset):
    dataset_format = 'csv' if '.csv' in dataset else 'sql'

    if UpdateTime.objects.filter(dataset=dataset).exists():
        last_update = UpdateTime.objects.get(dataset=dataset)
        time_delta = datetime.datetime.now().timestamp() - last_update.timestamp
        print(datetime.datetime.now().timestamp())
        print(last_update.timestamp)
        print(time_delta)
        if time_delta < last_update.refresh_rate:
            if dataset_format == 'csv':
                df = pd.read_csv(dataset)
            elif dataset_format == 'sql':
                df = pd.read_sql()

                df.to_csv(location, index=False)
    else:

        last_update = UpdateTime.objects.create(dataset=dataset, dataset_format=dataset_format, success=False,
                                                timestamp=datetime.datetime(1970, 1, 1))





