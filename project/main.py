import asyncio
from app import run

# while True:
#     user_input = input("\nPlease ask=> ")
#     if not user_input:
#         user_input = "give me Headphone products"
#     if user_input.lower() == "exit":
#         break

user_inputs = [
    # General
    # "Hi",
    # "can you help me",
    # get_current_weather
    # "give me the weather now in errachidia",
    # search_product
    # "give me Headphone products",
    # get_crypto_price
    "give me the current price of BITCOIN",
    # get_joke
    "give me a joke"
]

for user_input in user_inputs:
    print("\nQuestion =>", user_input)
    asyncio.run(run("llama3.2:3b", user_input))