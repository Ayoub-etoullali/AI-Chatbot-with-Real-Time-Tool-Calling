import json
import requests

def get_product_by_name(product_name: str):
    """Get available E-commerce Products by product name"""
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