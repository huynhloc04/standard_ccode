import openai
import json
from pprint import pprint

openai.api_key = open("key.txt", "r").read()

def get_pizza_info(pizza_name):
    pizza_info = {
        "name": pizza_name,
        "price": "$10.99"
    }
    return json.dumps(pizza_info)

#   If you want to return a nicely response to user
def get_response(query):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-0613',
        messages=[{"role": "user",
                  "content": query}],
        functions=[
            {
                "name": "get_pizza_info",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pizza_name": {"type": "string"},
                        "location": {"type": "string"},
                    },
                    "required": ["pizza_name"]                                
                },                
            },
        ],
        function_call='auto'    #   {"name": "get_pizza_info"} or "auto" or "none"
    )

    message = response["choices"][0]["message"]

    if message.get("function_call"):
        function_name = message["function_call"]["name"]
        #   Get the JSON output from functions properties. At this time, "get_pizza_info" function hasn't called yet
        function_args = json.loads(message["function_call"]["arguments"])
        #   Get the output from function after calling
        function_response = get_pizza_info(
            pizza_name=function_args.get("pizza_name"),
        )

        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "query"},
                message,
                {"role": "function",
                 "name": function_name,
                 "content": function_response,
                 },
            ],
        )
        return second_response.choices[0].message.content
    return message


#   If you want only json format return that get information from your query. Although "get_pizza_info" function is called, but the response doesn't get any 
#   information about the "get_pizza_info" function
def get_json(query):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo-0613',
        messages=[{"role": "user",
                  "content": query}],
        functions=[
            {
                "name": "get_pizza_info",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pizza_name": {"type": "string"},
                        "nation": {"type": "string"}
                    }                              
                },
            },
        ],
        function_call={"name": "get_pizza_info"}    #   Alway define the param like this if you want to get JSON format response.   
    ).choices[0].message

    func_arg = response["function_call"]["arguments"]

    return func_arg


if __name__ == "__main__":
    func_call = input("Do you want a JSON response? Type (y/n): ")

    if func_call.lower() == "y":
        response = get_json("How much does Calzone pizza cost in Vietnam?")
    else:
        response = get_response("How much does Calzone pizza cost in Vietnam?")

    print("\n >>> Response", response)








