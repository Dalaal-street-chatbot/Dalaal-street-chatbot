import yfinance as yf

def get_stock_price(symbol: str) -> dict:
	try:
		ticker = yf.Ticker(symbol + ".NS")  # .NS for NSE, .BO for BSE
		data = ticker.history(period="1d")
		if not data.empty:
			latest_price = data['Close'].iloc[-1]
			return {"symbol": symbol, "price": latest_price}
		else:
			return {"error": f"Could not retrieve data for {symbol}"}
	except Exception as e:
		return {"error": f"An error occurred: {e}"}

# You can add more functions here for news, etc.