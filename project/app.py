import ollama, json
from functions import get_product_by_name

# --- Async assistant runner ---
async def run(model: str, user_input: str):
    client = ollama.AsyncClient()
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. "
                "Only call tools if the user explicitly asks for **E-Commerce Products**. "
                "When showing results from tools, answer briefly and clearly. "
                "Do not mention datasets, tables, or add extra explanations. "
                "If the user says something like 'hi', 'hello', or general chat, just respond normally without tools."
            ),
        },
        {"role": "user", "content": user_input},
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_product_by_name",
                "description": "Get available E-commerce Products by product name",
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
        "get_product_by_name": get_product_by_name,
    }

    for tool in response["message"]["tool_calls"]:
        print("\nTool call:", tool)
        func_name = tool["function"]["name"]
        func_args = tool["function"]["arguments"]
        function_to_call = available_functions[func_name]
        
        if func_name == "get_product_by_name":
            # if not func_args["product_name"]:
            #     func_args["product_name"] = "Headphones"
            function_response = function_to_call(func_args["product_name"])
        else:
            # Extract parameters if present
            # params = tool["function"].get("parameters", {})
            # function_response = function_to_call(**params)
            function_response = function_to_call()
            
        print("\nFunction Response:", function_response)

    messages.append({"role": "tool", "content": json.dumps(function_response)})

    response = await client.chat(model=model, messages=messages)
    print("\nAssistant (with tool call):", response["message"]["content"])