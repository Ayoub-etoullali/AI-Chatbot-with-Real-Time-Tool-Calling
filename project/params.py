import pandas as pd
import random, requests

######################################## Address Coordinate

def get_coords_from_address(address):
    url = "https://nominatim.openstreetmap.org/search"
    param = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "AYOUB/1.0"  # Nominatim requires a User-Agent
    }
    response = requests.get(url, params=param, headers=headers)
    data = response.json()
    if data:
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return str(lat)+","+str(lon)
    else:
        return None

######################################## E-Commerce Products

# Base product types
product_types = [
    "Wireless Headphones", "Smartphone Case", "Laptop Stand", "Bluetooth Speaker",
    "Gaming Mouse", "LED Desk Lamp", "Backpack", "Fitness Tracker",
    "Coffee Maker", "Smartwatch", "Portable Charger", "Desk Organizer",
    "Water Bottle", "Yoga Mat", "Sunglasses", "T-Shirt", "Running Shoes",
    "Electric Toothbrush", "Camera Tripod", "Noise Cancelling Earbuds"
]

# Descriptors to make products unique
adjectives = [
    "Pro", "Max", "Mini", "Ultra", "Eco", "Travel", "Premium", "Deluxe",
    "Compact", "Lightweight", "Portable", "Wireless", "Smart", "Advanced"
]

# Generate 100 product names
products = [
    f"{random.choice(adjectives)} {random.choice(product_types)}"
    for _ in range(100)
]

# Generate random prices between $10 and $1000
prices = [round(random.uniform(10, 1000), 2) for _ in range(100)]

# Currency (all USD)
currency = ["USD"] * 100

# Create DataFrame
STOCK = pd.DataFrame({
    "symbol": [f"PROD{i:03}" for i in range(1, 101)],
    "name": products,
    "price": prices,
    "currency": currency
})

# Save to CSV
STOCK.to_csv("../data/stock_data.csv", index=False)
print("Generated stock_data.csv with 100 e-commerce products!")
