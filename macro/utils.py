import pandas as pd


def get_inflation_color(value):
    if value > 10:
        color = 'red'
    elif value > 6:
        color = 'orange'
    elif value > 3:
        color = 'yellow'
    elif value > 0:
        color = 'green'
    elif value == 0 or pd.isna(value):
        color = 'white'
    else:
        color = 'blue'

    return f"""<p style="color:{color};">{str(value.__round__(2))}%</p>"""

def get_debt_color(value):
    if value > 100:
        color = 'red'
    elif value > 70:
        color = 'orange'
    elif value > 35:
        color = 'yellow'
    elif value == 0 or pd.isna(value):
        color = 'white'
    else:
        color= 'green'
    return f"""<p style="color:{color};">{str(value.__round__(2))}%</p>"""


def get_gdp_color(value):
    if value > 4:
        color = 'green'
    elif value > 1:
        color = 'yellow'
    elif value > 0:
        color = 'orange'
    elif value < 0:
        color = 'red'
    else:
        color = 'white'
    return f"""<p style="color:{color};">{str(value.__round__(2))}%</p>"""