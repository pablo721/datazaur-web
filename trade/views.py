from django.shortcuts import render
from django.views.generic import TemplateView


class TradeView(TemplateView):
	template_name = 'trade/trade.html'


class MomentumView(TemplateView):
	template_name = 'trade/momentum.html'


class ArbitrageView(TemplateView):
	template_name = 'trade/arbitrage.html'


class StatArbView(TemplateView):
	template_name = 'trade/stat_arb.html'


class SignalsView(TemplateView):
	template_name = 'trade/signals.html'


class InsiderTradesView(TemplateView):
	template_name = 'trade/inisder_trades.html'



