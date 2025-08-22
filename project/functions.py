import requests, json, os
from bs4 import BeautifulSoup
from params import get_coords_from_address

def get_current_weather(city):
    """Get the current weather in a given city"""
    latitude, longitude = get_coords_from_address(city)
    base = "https://api.openweathermap.org/data/2.5/weather"
    key = os.environ['WEATHERMAP_API_KEY']
    request_url = f"{base}?lat={latitude}&lon={longitude}&appid={key}&units=metric"
    response = requests.get(request_url)
    
    result = {
        "latitude": latitude,
        "longitude": longitude,
        **response.json()["main"]
    }
    return json.dumps(result)

def search_product(product_name: str):
    """Returns E-commerce Products whose name contains the query string (case-insensitive)"""
    """
    Args:
        product_name (str): Name or partial name of the product to search.
    Returns:
        list: List of matching products with their symbol, name, price, and currency.
    """
    url = "http://127.0.0.1:5000/search_product"
    params = {"query": product_name}
    response = requests.get(url, params=params)

    return json.dumps(response.json(), indent=2)

def get_crypto_price(crypto_name: str) -> str:
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
            "ids": crypto_name.lower(),
            "vs_currencies": "usd"
        }
        response = requests.get(url, params=params)

        if response.status_code != 200:
            return json.dumps({"error": f"Error fetching data: {response.status_code}"})

        data = response.json()
        if crypto_name.lower() not in data:
            return json.dumps({"error": f"Sorry, I couldn’t find price data for '{crypto_name.upper()}'."})

        price = data[crypto_name.lower()]["usd"]
        return json.dumps({f"{crypto_name.upper()}": f"{price:,.2f} USD"})

    except Exception as e:
        return json.dumps({"error": f"Error: {str(e)}"})

def get_info_from_portfolio() -> str:
    """Retrieve information about Ayoub ETTOULLAI from his portfolio."""
    url = "https://ayoub-etoullali.netlify.app/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract headings and paragraphs
    headings = [h.text for h in soup.find_all(['h1', 'h2', 'h3'])]
    paragraphs = [p.text for p in soup.find_all('p')]

    # Combine results
    info = headings + paragraphs
    return json.dumps({"portfolio": info})

def get_joke() -> str:
    """Return a random joke."""
    response = requests.get("https://official-joke-api.appspot.com/random_joke").json()
    return json.dumps({"joke": f"{response['setup']} - {response['punchline']}"})
