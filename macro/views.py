from django.shortcuts import render
from django.views.generic import TemplateView
import os
import pandas as pd
from sqlalchemy import create_engine
from .forms import *
#from .markets_src import *
from website.models import *
from config import constants
from .utils import get_debt_color, get_inflation_color, get_gdp_color
from src.utils.formatting import color_cell2




class MacroView(TemplateView):
    template_name = 'macro/macro.html'

    def get_context_data(self, **kwargs):
        engine = create_engine(os.environ.get('LOCAL_DB_URL'))
        df = pd.read_sql('select * from macro.macro_stats', engine, index_col='Country')
        df['inflation'] = df['inflation'].apply(get_inflation_color)
        df['gdp'] = df['gdp'].apply(get_gdp_color)
        df['debt-to-gdp'] = df['debt-to-gdp'].apply(get_debt_color)

        print(df)
        return {'df': df.to_html(escape=False)}
class InflationView(TemplateView):
    template_name = 'macro/macro.html'


    def get_context_data(self, **kwargs):
        engine = create_engine(os.environ.get('LOCAL_DB_URL'))
        df = pd.read_sql('select * from macro.inflation_hcpi', engine, index_col='index')
        df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: x.replace('no data', None))
        df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: x.__round__(2))
        df.index.name = 'Inflation YoY'
        return {'df': df.to_html()}


class DebtView(TemplateView):
    template_name = 'macro/macro.html'

    def get_context_data(self, **kwargs):
        engine = create_engine(os.environ.get('LOCAL_DB_URL'))
        df = pd.read_sql('select * from macro.govt_debt', engine, index_col='index')
        df.index.name = 'year'
        return {'df': df.to_html()}


class GDPView(TemplateView):
    template_name = 'macro/macro.html'


    def get_context_data(self, **kwargs):
        engine = create_engine(os.environ.get('LOCAL_DB_URL'))
        df = pd.read_sql('select * from macro.real_gdp_growth', engine, index_col='index')
        df.index.name = 'year'
        return {'df': df.to_html()}