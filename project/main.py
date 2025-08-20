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
    "Hi",
    "i need help",
    # get_product_by_name
    "give me Headphone products",
]

for user_input in user_inputs:
    print("\nQuestion =>", user_input)
    asyncio.run(run("llama3.2:3b", user_input))