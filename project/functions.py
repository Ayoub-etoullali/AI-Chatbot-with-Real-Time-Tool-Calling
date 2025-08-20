import requests, json, os
from params import get_coords_from_address

def get_current_weather(address):
    """Get the current weather in a given city or address name"""
    latitude, longitude = get_coords_from_address(address)
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
    Fetch products from the local Flask API filtered by product name.
    Args:
        product_name (str): Name or partial name of the product to search.
    Returns:
        list: List of matching products with their symbol, name, price, and currency.
    """
    url = "http://127.0.0.1:5000/search_product"
    params = {"query": product_name}
    response = requests.get(url, params=params)

    return json.dumps(response.json(), indent=2)