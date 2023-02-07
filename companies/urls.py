from django.urls import path, include
from django.contrib.auth.decorators import login_required, permission_required
from . import views


app_name = 'companies'
urlpatterns = [
    path('', views.SearchView.as_view(), name='search'),
    path('<str:symbol>/overview', views.OverviewView.as_view(), name='overview'),
    path('<str:symbol>/market_data', views.MarketDataView.as_view(), name='market_data'),
    path('<str:symbol>/income_statement', views.IncomeStatementView.as_view(), name='income_statement'),
    path('<str:symbol>/balance_sheet', views.BalanceSheetView.as_view(), name='balance_sheet'),
    path('<str:symbol>/cash_flow', views.CashFlowView.as_view(), name='cash_flow'),
    # path('<str:symbol>/ratios', views.RatiosView.as_view(), name='ratios'),
    # path('<str:symbol>/insider_sentiment', views.InsiderSentimentView.as_view(), name='insider_sentiment'),
    # path('<str:symbol>/options', views.OptionsView.as_view(), name='options'),
    # path('<str:symbol>/ownership', views.OwnershipView.as_view(), name='ownership'),
    # path('<str:symbol>/recommendations', views.RecommendationsView.as_view(), name='recommendations'),
    # path('<str:symbol>/related_news', views.RelatedNewsView.as_view(), name='related_news'),
    # path('<str:symbol>/enterprise_value', views.EnterpriseValueView.as_view(), name='enterprise_value'),
    ]

