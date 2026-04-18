from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import create_transaction
from .views import (
    portfolio_list,
    watchlist_list,
    login_api,
    logout_api,
    me_api,
    register_api,
    transaction_list,delete_stock,portfolio_summary,api_home
)

schema_view = get_schema_view(
    openapi.Info(
        title="Investment API",
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('login/', login_api),
    path('logout/', logout_api),
    path('me/', me_api),
    path('portfolio/', portfolio_list),
    path('portfolio/delete/<str:stock_symbol>/', delete_stock),
    path('watchlist/', watchlist_list),
    path('transaction/', create_transaction),
    path("register/", register_api),
    path("transactions/", transaction_list),
    path('portfolio-summary/', portfolio_summary),
    path('', api_home),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),

]
