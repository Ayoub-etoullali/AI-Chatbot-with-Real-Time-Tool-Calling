import json, requests

def get_crypto_price(symbol: str) -> str:
    """Returns the current cryptocurrency price in USD."""
    """
    Args:
        symbol (str): The cryptocurrency symbol (e.g., 'BTC', 'ETH').
    Returns:
        str: A formatted string with the current price or an error message.
    """
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": symbol.lower(),
            "vs_currencies": "usd"
        }
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return f"Error fetching data: {response.status_code}"

        data = response.json()
        if symbol.lower() not in data:
            return f"Sorry, I couldn’t find price data for '{symbol.upper()}'."

        price = data[symbol.lower()]["usd"]
        return f"The current price of {symbol.upper()} is ${price:,.2f} USD."

    except Exception as e:
        return f"Error: {str(e)}"
  
print(get_crypto_price("Ethereum"))