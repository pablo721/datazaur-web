from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.dateparse import parse_datetime
import investpy
from .models import MacroCalendar, CryptoCalendar, IPOCalendar, EarningsCalendar
from sqlalchemy import create_engine
import os
import pandas as pd

class MacroCalendarView(TemplateView):
    engine = create_engine(os.environ.get('LOCAL_DB_URL'))
    template_name = 'calendar_/macro_calendar.html'

    def get_context_data(self, **kwargs):
        return {'calendar': MacroCalendar.objects.all(),
                'columns': [f.name for f in MacroCalendar._meta.get_fields()]}


class CryptoCalendarView(TemplateView):
    engine = create_engine(os.environ.get('LOCAL_DB_URL'))
    template_name = 'calendar_/calendar_df.html'


    def get_context_data(self, **kwargs):
        df = pd.read_sql('select * from calendar.crypto_calendar_calendar', self.engine)
        df['date_event'] = df['date_event'].apply(lambda x: str(x)[:10])
        df['created_date'] = df['created_date'].apply(lambda x: str(x)[:10])
        df['proof'] = df['proof'].apply(lambda x: f'<img src="{x}" width=60 height=60>')
        df['source'] = df['source'].apply(lambda x: f'<a href="{x}"> Coinmarketcal </a>')
        return {'df': df.to_html(escape=False)}

    # def get_context_data(self, **kwargs):
    #     calendar = CryptoCalendar.objects.all()
    #
    #     for event in calendar:
    #          event.date_event = (event.date_event)
    #
    #     return {'calendar': calendar,
    #             'columns': [f.name for f in CryptoCalendar._meta.get_fields()]}


class IPOCalendarView(TemplateView):
    engine = create_engine(os.environ.get('LOCAL_DB_URL'))
    template_name = 'calendar_/calendar_df.html'

    def get_context_data(self, **kwargs):
        return {'df': pd.read_sql('select * from calendar.ipo_calendar_calendar', self.engine).to_html()}


    # def get_context_data(self, **kwargs):
    #     return {'calendar': IPOCalendar.objects.all(),
    #             'columns': [f.name for f in IPOCalendar._meta.get_fields()]}


class EarningsCalendarView(TemplateView):
    engine = create_engine(os.environ.get('LOCAL_DB_URL'))
    template_name = 'calendar_/calendar_df.html'


    def get_context_data(self, **kwargs):
        return {'df': pd.read_sql('select * from calendar.earnings_calendar_calendar', self.engine).to_html()}

    # def get_context_data(self, **kwargs):
    #     return {'calendar': pd.read_sql('calendar.earnings_calendar_calendar'),
    #             'columns': [f.name for f in EarningsCalendar._meta.get_fields()]}
