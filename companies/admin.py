from django.contrib import admin
from .models import Company, IncomeStatement, BalanceSheet, CashFlowStatement, Recommendation


admin.site.register(Company)
admin.site.register(IncomeStatement)
admin.site.register(BalanceSheet)
admin.site.register(Recommendation)
