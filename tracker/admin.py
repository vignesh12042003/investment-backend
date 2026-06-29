from django.contrib import admin

from .models import (
    Asset,
    Wallet,
    Holding,
    Transaction,
    Watchlist,
    Goal,
    InvestmentNote,
)

admin.site.register(Asset)
admin.site.register(Wallet)
admin.site.register(Holding)
admin.site.register(Transaction)
admin.site.register(Watchlist)
admin.site.register(Goal)
admin.site.register(InvestmentNote)