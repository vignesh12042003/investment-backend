from urllib import request

from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .services import calculate_portfolio_value
from rest_framework_simplejwt.tokens import RefreshToken

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
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def portfolio_list(request):

    print("USER:", request.user)
    print("AUTH:", request.auth)

    # ---------------- GET (VIEW PORTFOLIO) ----------------
    if request.method == 'GET':
        portfolio = Portfolio.objects.filter(user=request.user)
        serializer = PortfolioSerializer(portfolio, many=True)

        return Response(serializer.data, status=200)

    # ---------------- POST (BUY STOCK) ----------------
    elif request.method == 'POST':
        stock_symbol = request.data.get('stock_symbol')
        quantity = request.data.get('total_quantity')
        price = request.data.get('avg_buy_price')

        # 🔍 VALIDATION
        if not stock_symbol or not quantity or not price:
            return Response(
                {"error": "stock_symbol, total_quantity, avg_buy_price are required"},
                status=400
            )

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            return Response(
                {"error": "Invalid data type for quantity or price"},
                status=400
            )

        # 🔄 CREATE OR UPDATE PORTFOLIO
        portfolio, created = Portfolio.objects.get_or_create(
            user=request.user,
            stock_symbol=stock_symbol,
            defaults={
                'total_quantity': quantity,
                'avg_buy_price': price
            }
        )

        if not created:
            total_cost = (portfolio.total_quantity * portfolio.avg_buy_price) + (quantity * price)
            total_quantity = portfolio.total_quantity + quantity

            portfolio.total_quantity = total_quantity
            portfolio.avg_buy_price = total_cost / total_quantity
            portfolio.save()

        return Response(
            {"message": "Stock added successfully"},
            status=201
        )

    # ---------------- FALLBACK ----------------
    return Response({"error": "Invalid request method"}, status=405)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def delete_stock(request, stock_symbol):

    try:
        portfolio = Portfolio.objects.get(user=request.user, stock_symbol=stock_symbol)
        portfolio.delete()
        return Response({"message": "Stock removed"})
    
    except Portfolio.DoesNotExist:
        return Response({"error": "Stock not found"}, status=404)

# ---------------- WATCHLIST ----------------
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
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
def login_api(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })

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
@authentication_classes([JWTAuthentication])
def me_api(request):
    return Response({"username": request.user.username})

# ---------------- BUY / SELL TRANSACTION ----------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def create_transaction(request):

    serializer = TransactionSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    stock_symbol = serializer.validated_data["stock_symbol"]
    transaction_type = serializer.validated_data["transaction_type"]
    quantity = serializer.validated_data["quantity"]

    # Fetch live price
    ticker = yf.Ticker(stock_symbol)
    price = ticker.history(period="1d")["Close"].iloc[-1]

    # -------- PRE-VALIDATION (SELL) --------
    if transaction_type == "SELL":
        portfolio = Portfolio.objects.filter(
            user=request.user,
            stock_symbol=stock_symbol
        ).first()

        if not portfolio or portfolio.total_quantity < quantity:
            return Response(
                {"error": "Not enough shares to sell"},
                status=400
            )

    # -------- SAVE TRANSACTION --------
    Transaction.objects.create(
        user=request.user,
        stock_symbol=stock_symbol,
        transaction_type=transaction_type,
        quantity=quantity,
        price=price,
    )

    # -------- UPDATE PORTFOLIO --------
    portfolio, created = Portfolio.objects.get_or_create(
        user=request.user,
        stock_symbol=stock_symbol,
        defaults={
            "total_quantity": 0,
            "avg_buy_price": 0
        }
    )

    if transaction_type == "BUY":
        total_cost = (portfolio.total_quantity * portfolio.avg_buy_price) + (quantity * price)
        total_qty = portfolio.total_quantity + quantity

        portfolio.total_quantity = total_qty
        portfolio.avg_buy_price = total_cost / total_qty

    elif transaction_type == "SELL":
        if portfolio.total_quantity < quantity:
            return Response({"error": "Not enough shares"}, status=400)

        portfolio.total_quantity -= quantity

        if portfolio.total_quantity == 0:
            portfolio.delete()
            return Response(
                {"message": "Stock sold completely"},
                status=200
            )

    portfolio.save()

    return Response(
        {"message": f"{transaction_type} transaction successful"},
        status=201
    )
# ---------------- REGISTER ----------------
@api_view(["POST"])
@permission_classes([AllowAny])
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
@authentication_classes([JWTAuthentication])
def transaction_list(request):
    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by("-created_at")
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def portfolio_summary(request):
    portfolio = Portfolio.objects.filter(user=request.user)

    data = calculate_portfolio_value(portfolio)

    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])  # 🔥 THIS FIX
def api_home(request):
    return Response({
        "message": "Investment Tracker API is running",
        "endpoints": [
            "/api/login/",
            "/api/token/",
            "/api/portfolio/",
            "/api/transaction/",
            "/api/portfolio-summary/"
        ]
    })