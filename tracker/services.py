import yfinance as yf
from django.core.cache import cache

def get_stock_price(symbol):
    price = cache.get(symbol)

    if not price:
        ticker = yf.Ticker(symbol)
        price = ticker.history(period="1d")["Close"].iloc[-1]
        price = round(float(price), 2)
        cache.set(symbol, price, timeout=300)
    return price

def calculate_portfolio_value(portfolio_items):
    total_investment = 0
    current_value = 0
    detailed_data = []

    for item in portfolio_items:
        quantity = item.total_quantity
        buy_price = item.avg_buy_price
        symbol = item.stock_symbol

        current_price = get_stock_price(symbol)

        invested = buy_price * quantity
        current = current_price * quantity

        total_investment += invested
        current_value += current

        detailed_data.append({
            "stock_symbol": symbol,
            "quantity": quantity,
            "avg_buy_price": buy_price,
            "current_price": current_price,
            "invested": invested,
            "current_value": current,
            "profit_loss": current - invested
        })

    return {
        "summary": {
            "total_investment": total_investment,
            "current_value": current_value,
            "profit_loss": current_value - total_investment
        },
        "stocks": detailed_data
    }