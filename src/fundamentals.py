import yfinance
import pandas as pd


class FundamentalData:
    def __init__(self, ticker):
        self.data = yfinance.Ticker(ticker)
        self.summary = self.data.info.pop('longBusinessSummary')
        for table in [self.data.balance_sheet, self.data.financials, self.data.cashflow]:
            table.columns = list(map(lambda x: str(x)[:10], table.columns))

    def get_fundamentals(self):
        return {'ticker': self.data.ticker,
                'isin': self.data.isin,
                'summary': self.summary,
                'info': pd.DataFrame(pd.Series(self.data.info)).to_html(escape=True),
                   'balance_sheet': self.data.balance_sheet.to_html(escape=False),
                   'financials': self.data.financials.to_html(escape=False),
                   'cashflow': self.data.cashflow.astype('float64').to_html(escape=False),
                   'earnings': self.data.earnings.to_html(escape=False),
                   'calendar': self.data.calendar.to_html(escape=False),
                   'major_holders': self.data.major_holders.to_html(escape=False),
                   'mutualfund_holders': self.data.mutualfund_holders.to_html(escape=False),
                   'institutional_holders': self.data.institutional_holders.to_html(escape=False),
                   'actions': self.data.actions.to_html(escape=False),
                   'options': self.data.options,
                   'recommendations': self.data.recommendations.to_html(escape=False),
                   'esg': self.data.sustainability.to_html(escape=False)}



    def get_price_history(self):
        context = {'price_history': self.data.history()}
        return context


