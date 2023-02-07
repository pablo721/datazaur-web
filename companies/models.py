from django.db import models


# 52WeekChange - o52WeekChange  ;  zip -> zip0  yield -> yield0  open -> open0
class Company(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['symbol', 'exchange'], name='unique_symbol_exchange'
            )
        ]

    shortName = models.CharField(max_length=64, null=True, blank=True)
    longName = models.CharField(max_length=64, null=True, blank=True)
    symbol = models.CharField(max_length=16, null=True, blank=True)
    website = models.CharField(max_length=64)
    #messageBoardId = models.CharField(max_length=64, null=True, blank=True)
    sector = models.CharField(max_length=64, null=True, blank=True)
    industry = models.CharField(max_length=64, null=True, blank=True)
    longBusinessSummary = models.CharField(max_length=2048, null=True, blank=True)
    logo_url = models.CharField(max_length=128, blank=True, null=True)
    financialCurrency = models.CharField(max_length=16, null=True, blank=True)
    fullTimeEmployees = models.IntegerField(null=True, blank=True)

    country = models.CharField(max_length=64, null=True, blank=True)
    state = models.CharField(max_length=64, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    address = models.CharField(max_length=64, null=True, blank=True)
    zip_code = models.CharField(max_length=16, null=True, blank=True)
    phone = models.CharField(max_length=64, null=True, blank=True)

    currentPrice = models.FloatField(null=True, blank=True)
    previousClose = models.FloatField(null=True, blank=True)
    beta = models.FloatField(null=True, blank=True)
    recommendationKey = models.CharField(max_length=64, null=True, blank=True)
    exchange = models.CharField(max_length=64, null=True, blank=True)
    quoteType = models.CharField(max_length=16, null=True, blank=True)

    marketCap = models.FloatField(null=True, blank=True)
    enterpriseValue = models.BigIntegerField(null=True, blank=True)
    sharesOutstanding = models.BigIntegerField(null=True, blank=True)
    floatShares = models.FloatField(null=True, blank=True)
    sharesShort = models.IntegerField(null=True, blank=True)
    shortPercentOfFloat = models.FloatField(null=True, blank=True)

    bookValue = models.FloatField(null=True, blank=True)
    priceToBook = models.FloatField(null=True, blank=True)
    shortRatio = models.FloatField(null=True, blank=True)
    pegRatio = models.FloatField(null=True, blank=True)
    debtToEquity = models.FloatField(null=True, blank=True)
    trailingPE = models.FloatField(null=True, blank=True)

    ebitdaMargins = models.FloatField(null=True, blank=True)
    profitMargins = models.FloatField(null=True, blank=True)
    grossMargins = models.FloatField(null=True, blank=True)
    operatingMargins = models.FloatField(null=True, blank=True)

    dividendRate = models.FloatField(null=True, blank=True)
    exDividendDate = models.FloatField(null=True, blank=True)
    lastDividendDate = models.DateField(null=True, blank=True)
    lastDividendValue = models.FloatField(null=True, blank=True)
    dividendYield = models.FloatField(null=True, blank=True)
    netIncomeToCommon = models.FloatField(null=True, blank=True)
    returnOnEquity = models.FloatField(null=True, blank=True)

    lastSplitDate = models.DateField(null=True, blank=True)
    lastSplitFactor = models.CharField(max_length=8, null=True, blank=True)

    heldPercentInsiders = models.FloatField(null=True, blank=True)
    heldPercentInstitutions = models.FloatField(null=True, blank=True)



class IncomeStatement(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'report_date'], name='unique_company_report_date'
            )
        ]
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='company_income_statement')
    report_date = models.DateField()
    Research_Development = models.FloatField(blank=True, null=True)
    Effect_Of_Accounting_Charges = models.FloatField(blank=True, null=True)
    Income_Before_Tax = models.FloatField(blank=True, null=True)
    Minority_Interest = models.FloatField(blank=True, null=True)
    Net_Income = models.FloatField(blank=True, null=True)
    Selling_General_Administrative = models.FloatField(blank=True, null=True)
    Gross_Profit = models.FloatField(blank=True, null=True)
    Ebit = models.FloatField(blank=True, null=True)
    Operating_Income = models.FloatField(blank=True, null=True)
    Other_Operating_Expenses = models.FloatField(blank=True, null=True)
    Interest_Expense = models.FloatField(blank=True, null=True)
    Extraordinary_Items = models.FloatField(blank=True, null=True)
    Non_Recurring = models.FloatField(blank=True, null=True)
    Other_Items = models.FloatField(blank=True, null=True)
    Income_Tax_Expense = models.FloatField(blank=True, null=True)
    Total_Revenue = models.FloatField(blank=True, null=True)
    Total_Operating_Expenses = models.FloatField(blank=True, null=True)
    Cost_Of_Revenue = models.FloatField(blank=True, null=True)
    Total_Other_Income_Expense_Net = models.FloatField(blank=True, null=True)
    Discontinued_Operations = models.FloatField(blank=True, null=True)
    Net_Income_From_Continuing_Ops = models.FloatField(blank=True, null=True)
    Net_Income_Applicable_To_Common_Shares = models.FloatField(blank=True, null=True)


class BalanceSheet(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['company_id', 'report_date'], name='unique_company_report_date2'
            )
        ]
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='company_balance_sheet')
    report_date = models.DateField()
    Intangible_Assets = models.FloatField(blank=True, null=True)
    Capital_Surplus = models.FloatField(blank=True, null=True)
    Total_Liab = models.FloatField(blank=True, null=True)
    Total_Stockholder_Equity = models.FloatField(blank=True, null=True)
    Other_Current_Liab = models.FloatField(blank=True, null=True)
    Total_Assets = models.FloatField(blank=True, null=True)
    Common_Stock = models.FloatField(blank=True, null=True)
    Other_Current_Assets = models.FloatField(blank=True, null=True)
    Retained_Earnings = models.FloatField(blank=True, null=True)
    Other_Liab = models.FloatField(blank=True, null=True)
    Good_Will = models.FloatField(blank=True, null=True)
    Treasury_Stock = models.FloatField(blank=True, null=True)
    Other_Assets = models.FloatField(blank=True, null=True)
    Cash = models.FloatField(blank=True, null=True)
    Total_Current_Liabilities = models.FloatField(blank=True, null=True)
    Deferred_Long_Term_Asset_Charges = models.FloatField(blank=True, null=True)
    Short_Long_Term_Debt = models.FloatField(blank=True, null=True)
    Other_Stockholder_Equity = models.FloatField(blank=True, null=True)
    Property_Plant_Equipment = models.FloatField(blank=True, null=True)
    Total_Current_Assets = models.FloatField(blank=True, null=True)
    Long_Term_Investments = models.FloatField(blank=True, null=True)
    Net_Tangible_Assets = models.FloatField(blank=True, null=True)
    Net_Receivables = models.FloatField(blank=True, null=True)
    Long_Term_Debt = models.FloatField(blank=True, null=True)
    Inventory = models.FloatField(blank=True, null=True)
    Accounts_Payable = models.FloatField(blank=True, null=True)
    Minority_Interest = models.FloatField(blank=True, null=True)


class CashFlowStatement(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['company_id', 'report_date'], name='unique_company_report_date1'
            )
        ]
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='company_cash_flow')
    report_date = models.DateField()
    Change_To_Liabilities = models.FloatField(blank=True, null=True)
    Total_Cashflows_From_Investing_Activities = models.FloatField(blank=True, null=True)
    Net_Borrowings = models.FloatField(blank=True, null=True)
    Total_Cash_From_Financing_Activities = models.FloatField(blank=True, null=True)
    Change_To_Operating_Activities = models.FloatField(blank=True, null=True)
    Net_Income = models.FloatField(blank=True, null=True)
    Change_In_Cash = models.FloatField(blank=True, null=True)
    Repurchase_Of_Stock = models.FloatField(blank=True, null=True)
    Total_Cash_From_Operating_Activities = models.FloatField(blank=True, null=True)
    Depreciation = models.FloatField(blank=True, null=True)
    Other_Cashflows_From_Investing_Activities = models.FloatField(blank=True, null=True)
    Dividends_Paid = models.FloatField(blank=True, null=True)
    Change_To_Inventory = models.FloatField(blank=True, null=True)
    Change_To_Account_Receivables = models.FloatField(blank=True, null=True)
    Other_Cashflows_From_Financing_Activities = models.FloatField(blank=True, null=True)
    Change_To_Netincome = models.FloatField(blank=True, null=True)
    Capital_Expenditures = models.FloatField(blank=True, null=True)


class Recommendation(models.Model):
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='company_recommendations')
    report_date = models.DateField()
    Firm = models.CharField(max_length=64)
    To_Grade = models.CharField(max_length=16)
    From_Grade = models.CharField(max_length=16)
    Action = models.CharField(max_length=16)


