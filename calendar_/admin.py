from django.contrib import admin

from .models import MacroCalendar, CryptoCalendar, IPOCalendar, EarningsCalendar

admin.site.register(MacroCalendar)
admin.site.register(CryptoCalendar)
admin.site.register(IPOCalendar)
admin.site.register(EarningsCalendar)


