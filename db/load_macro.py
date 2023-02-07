from sqlalchemy import create_engine
import pandas as pd
import os
import numpy as np

engine = create_engine(os.environ.get('LOCAL_DB_URL'))
print(os.getcwd())
def load_inflation():
    df = pd.read_excel('files/Inflation-data.xlsx', 'hcpi_a', index_col='Country').transpose().astype(np.double)
    df.to_sql('inflation_hcpi', engine, 'macro', if_exists='replace')


def load_debt():
    df = pd.read_excel('files/imf-debt.xls', 'CG_DEBT_GDP', index_col='Country').transpose()
    df.to_sql('govt_debt', engine, 'macro', if_exists='replace')


def load_gdp():
    df = pd.read_excel('files/imf-gdp.xls', 'NGDP_RPCH', index_col='Country').transpose()
    df.to_sql('real_gdp', engine, 'macro', if_exists='replace')

def load_macro():
    df_inf = pd.read_excel('files/Inflation-data.xlsx', 'hcpi_a', index_col='Country').transpose()
    df_debt = pd.read_excel('files/imf-debt.xls', 'CG_DEBT_GDP', index_col='Country').transpose()
    df_gdp = pd.read_excel('files/imf-gdp.xls', 'NGDP_RPCH', index_col='Country').transpose()
    year = max(df_inf.index)
    row_inf = df_inf.loc[year, :]
    row_debt = df_debt.loc[year, :]
    row_gdp = df_gdp.loc[year, :]
    df2 = pd.DataFrame(index=df_inf.columns[1:], columns=['inflation', 'debt-to-gdp', 'gdp'], data={'gdp': row_gdp,
                                                                                                    'inflation': row_inf,
                                                                                                    'debt-to-gdp': row_debt,
                                                                                                        })
    for col in df2.columns:
        df2[col] = df2[col].astype('string')
        df2[col] = df2[col].apply(lambda x: np.NaN if pd.isna(x) or x == 'no data' else float(x).__round__(2))

    df2.to_sql('macro_stats', engine, 'macro')



