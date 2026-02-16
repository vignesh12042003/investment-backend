from django.contrib import admin
from .models import Watchlist, Transaction, Portfolio

admin.site.register(Watchlist)
admin.site.register(Transaction)
admin.site.register(Portfolio)
