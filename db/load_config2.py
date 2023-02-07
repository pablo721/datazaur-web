from sqlalchemy import create_engine
import yaml
import os
import pandas as pd


def load_config(url):
    engine = create_engine(url)
    cfg_dir = os.path.join(os.getcwd(), 'config')
    cfg = os.path.join(cfg_dir, 'config.yaml')
    types = os.path.join(cfg_dir, 'types.yaml')
    keys = os.path.join(cfg_dir, 'keys.yaml')

    config = {}

    with open(cfg) as file:
        config['config'] = yaml.safe_load(file)

    with open(keys) as file:
        config['keys'] = yaml.safe_load(file)

    with open(types) as file:
        config['types'] = yaml.safe_load(file)

    types_df = config['types']



    config['asset_classes'] = types_df['asset_classes']
    config['commodity_groups'] = types_df['commodity_groups']
    config['source_types'] = types_df['source_types']



    for table in ['config', 'keys']:
        df = pd.DataFrame(pd.Series(config[table])).reset_index(drop=False)
        df.columns = ['key', 'value']
        print(f'Loading {table}...')
        df.to_sql(table, engine, 'config', if_exists='replace', index=False)
        print(f'Loaded {table}.')

    for table in ['asset_classes', 'commodity_groups', 'source_types']:
        df = pd.DataFrame(pd.Series(config[table]))
        print(df)
        col_name = table[:-1]
        df.columns = [col_name]
        print(f'Loading {table}...')
        df.loc[:, col_name].to_sql(table, engine, 'config', if_exists='replace', index=False)
        print(f'Loaded {table}.')




