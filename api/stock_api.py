import yfinance as yf

def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        price = stock.info.get("currentPrice", "Not available")
        return f"Current price of {symbol} is {price}"
    except Exception as e:
        return f"Error fetching stock data: {str(e)}"