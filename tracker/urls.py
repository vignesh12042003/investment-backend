from django.urls import path
from .views import create_transaction
from .views import (
    portfolio_list,
    watchlist_list,
    login_api,
    logout_api,
    me_api,
    register_api,
    transaction_list
)

urlpatterns = [
    path('login/', login_api),
    path('logout/', logout_api),
    path('me/', me_api),
    path('portfolio/', portfolio_list),
    path('watchlist/', watchlist_list),
    path('transaction/', create_transaction),
    path("register/", register_api),
    path("transactions/", transaction_list),

]
