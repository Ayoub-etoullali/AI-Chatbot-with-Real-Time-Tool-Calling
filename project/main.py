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
    # "Hello there!",
    # "Could you assist me?",
    # # get_current_weather
    # "What’s the current weather like in Errachidia?",
    # # search_product
    # "Can you show me some headphone options?",
    # # get_crypto_price
    # "What’s the latest price of Bitcoin?",
    # get_info_from_portfolio
    "What is Ayoub ETOULLALI",
    # get_joke
    # "Tell me a funny joke, please."
]

for user_input in user_inputs:
    print("\nQuestion =>", user_input)
    response = asyncio.run(run("llama3.2:3b", user_input))
    print(response)