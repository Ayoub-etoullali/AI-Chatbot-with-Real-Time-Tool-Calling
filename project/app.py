import ollama, json
from functions import get_current_weather, search_product, get_crypto_price, get_joke

# --- Async assistant runner ---
async def run(model: str, user_input: str):
    client = ollama.AsyncClient()
    messages = [
        {
            'role': 'system',
            'content': """
                You are a helpful assistant. Only call tools if the user explicitly asks for:
                **Weather**, **E-Commerce Products**, **Crypto Prices**, **Joke**.

                Return the content exactly as is, without adding extra commentary. 
                Do not mention datasets, tables, or add extra explanations.
                If the user says something like 'hi', 'hello', or general chat, just respond normally without tools.
            """
        },
        {
            "role": "user", 
            "content": user_input
        }
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given city or address name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "address_name": {
                        "type": "string",
                        "description": "The city or address name of a place",
                        }
                    },
                    "required": ["address_name"]
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "search_product",
                "description": "Returns E-commerce Products whose name contains the query string (case-insensitive)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_name": {
                            "type": "string",
                            "description": "The name of the product to filter E-Commerce Products"
                            }
                    },
                    "required": ["product_name"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_crypto_price",
                "description": "Returns the current cryptocurrency price in USD.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "crypto_name": {
                            "type": "string",
                            "description": "The cryptocurrency name (e.g. 'Ethereum', 'Bitcoin', 'Tether', etc)"
                            }
                    },
                    "required": ["crypto_name"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_joke",
                "description": "Return a random joke.",
                }
        }
    ]

    response = await client.chat(
        model=model,
        messages=messages,
        tools= tools,
    )

    if not response["message"].get("tool_calls"):
        print("\nAssistant (No tool call):", response["message"]["content"])
        return

    messages.append(response["message"])

    available_functions = {
        "get_current_weather": get_current_weather,
        "search_product": search_product,
        "get_crypto_price": get_crypto_price,
        "get_joke": get_joke
    }

    for tool in response["message"]["tool_calls"]:
        print("\nTool call:", tool)
        func_name = tool["function"]["name"]
        func_args = tool["function"]["arguments"]
        function_to_call = available_functions[func_name]
        
        if func_name == "get_current_weather":
            # if not func_args["address_name"]:
            #     func_args["address_name"] = "Errachidia"
            function_response = function_to_call(func_args["address_name"])
        elif func_name == "search_product":
            # if not func_args["product_name"]:
            #     func_args["product_name"] = "Headphones"
            function_response = function_to_call(func_args["product_name"])
        elif func_name == "get_crypto_price":
            # if not func_args["crypto_name"]:
            #     func_args["crypto_name"] = "Ethereum"
            function_response = function_to_call(func_args["crypto_name"])
        else:
            # Extract parameters if present
            # params = tool["function"].get("parameters", {})
            # function_response = function_to_call(**params)
            function_response = function_to_call()
            
        print("\nFunction Response:", function_response)

    messages.append(
        {
            "role": "tool", 
            "tool_name": func_name,
            "content": json.dumps(function_response)
        }
    )

    messages = [
        {
            'role': 'system',
            'content': """
                You are a helpful assistant. Only call tools if the user explicitly asks for:
                **Weather**, **E-Commerce Products**, **Crypto Prices**, **Joke**.

                Do not mention datasets, tables, or add extra explanations.
                If the user says something like 'hi', 'hello', or general chat, just respond normally without tools.
            """
        },
        {
            'role': 'user',
            'content': f"""
                Question: {user_input}
                repharse well the Answer from "{function_response}" as a helpful assistant
            """
        }
    ]
    response = await client.chat(model=model, messages=messages)
    print("\nAssistant (with tool call):", response["message"]["content"])