from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .authentication import CsrfExemptSessionAuthentication
from .models import Portfolio, Watchlist, Transaction
from .serializers import (
    PortfolioSerializer,
    WatchlistSerializer,
    TransactionSerializer,
)

import yfinance as yf


# ---------------- PORTFOLIO ----------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def portfolio_list(request):
    portfolio = Portfolio.objects.filter(user=request.user)
    data = []

    for p in portfolio:
        ticker = yf.Ticker(p.stock_symbol)
        price = ticker.history(period="1d")["Close"].iloc[-1]

        data.append({
            "stock_symbol": p.stock_symbol,
            "total_quantity": p.total_quantity,
            "avg_buy_price": p.avg_buy_price,
            "current_price": round(float(price), 2)
        })

    return Response(data)


# ---------------- WATCHLIST ----------------
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([CsrfExemptSessionAuthentication])
def watchlist_list(request):
    user = request.user

    if request.method == 'GET':
        watchlist = Watchlist.objects.filter(user=user)
        serializer = WatchlistSerializer(watchlist, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        stock_symbol = request.data.get("stock_symbol")

        if not stock_symbol:
            return Response({"error": "Stock symbol required"}, status=400)

        obj, created = Watchlist.objects.get_or_create(
            user=user,
            stock_symbol=stock_symbol.upper()
        )

        if not created:
            return Response({"error": "Stock already exists"}, status=400)

        return Response({"message": "Stock added"}, status=201)

    if request.method == 'DELETE':
        stock_symbol = request.data.get("stock_symbol")
        Watchlist.objects.filter(
            user=user,
            stock_symbol=stock_symbol
        ).delete()
        return Response({"message": "Stock removed"}, status=200)




# ---------------- LOGIN ----------------
@api_view(["POST"])
@authentication_classes([CsrfExemptSessionAuthentication])
def login_api(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user:
        login(request, user)
        return Response({"message": "Login successful"})
    return Response({"error": "Invalid credentials"}, status=401)


# ---------------- LOGOUT ----------------
@api_view(["POST"])
@authentication_classes([CsrfExemptSessionAuthentication])
def logout_api(request):
    logout(request)
    return Response({"message": "Logout successful"})


# ---------------- CURRENT USER ----------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_api(request):
    return Response({"username": request.user.username})


# ---------------- BUY / SELL TRANSACTION ----------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([CsrfExemptSessionAuthentication])
def create_transaction(request):
    serializer = TransactionSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    stock_symbol = serializer.validated_data["stock_symbol"]
    transaction_type = serializer.validated_data["transaction_type"]
    quantity = serializer.validated_data["quantity"]

    # Fetch live price from Yahoo
    ticker = yf.Ticker(stock_symbol)
    price = ticker.history(period="1d")["Close"].iloc[-1]

    # SELL validation
    if transaction_type == Transaction.SELL:
        portfolio = Portfolio.objects.filter(
            user=request.user, stock_symbol=stock_symbol
        ).first()

        if not portfolio or portfolio.total_quantity < quantity:
            return Response(
                {"error": "Not enough shares to sell"}, status=400
            )

    # Save transaction
    Transaction.objects.create(
        user=request.user,
        stock_symbol=stock_symbol,
        transaction_type=transaction_type,
        quantity=quantity,
        price=price,
    )

    # -------- UPDATE PORTFOLIO (ONLY PLACE) --------
    portfolio, created = Portfolio.objects.get_or_create(
    user=request.user,
    stock_symbol=stock_symbol,
    defaults={"total_quantity": 0, "avg_buy_price": 0},
)
    if transaction_type == Transaction.BUY:
        total_cost_existing = portfolio.total_quantity * portfolio.avg_buy_price
        total_cost_new = quantity * price

        new_total_quantity = portfolio.total_quantity + quantity

        portfolio.avg_buy_price = (
             (total_cost_existing + total_cost_new) / new_total_quantity
             if new_total_quantity > 0 else 0
               )
        portfolio.total_quantity = new_total_quantity
    elif transaction_type == Transaction.SELL:
        portfolio.total_quantity -= quantity
    # avg_buy_price remains unchanged on SELL
    if portfolio.total_quantity <= 0:
        portfolio.delete()
    else:
        portfolio.save()


    return Response(
        {"message": f"{transaction_type} transaction successful"},
        status=201,
    )


# ---------------- REGISTER ----------------
@api_view(["POST"])
@authentication_classes([CsrfExemptSessionAuthentication])
def register_api(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not email or not password:
        return Response(
            {"error": "Username, email, and password are required"},
            status=400,
        )

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists"}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already registered"}, status=400)

    User.objects.create_user(
        username=username, email=email, password=password
    )

    return Response({"message": "Account created successfully"}, status=201)


# ---------------- TRANSACTION HISTORY ----------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([CsrfExemptSessionAuthentication])
def transaction_list(request):
    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by("-created_at")
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)
