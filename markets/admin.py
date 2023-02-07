from django.contrib import admin
from .models import *

admin.site.register(Ticker)
admin.site.register(Stock)

admin.site.register(Currency)
admin.site.register(Commodity)
admin.site.register(Index)
admin.site.register(Exchange)



