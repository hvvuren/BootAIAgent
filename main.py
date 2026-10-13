import os
import sys
import argparse
import json
from openai import OpenAI
from dotenv import load_dotenv
from prompts import system_prompt
from call_function import available_functions, call_function

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("API key absent")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

for _ in range(20):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    message = response.choices[0].message
    messages.append(message)
    if message.tool_calls is not None:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            messages.append(result_message)
            if not result_message["content"]:
                raise Exception("Content absent from result message")
            if args.verbose:
                print(f"-> {result_message['content']}")
    else:
        if args.verbose:
            if response.usage is None:
                raise RuntimeError("Something has gone horribly wrong")
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
            print(response.choices[0].message.content)
            break
        else:
            print(response.choices[0].message.content)
            break
else:
    print("request has exceeded 20 iterations")
    sys.exit(1)
