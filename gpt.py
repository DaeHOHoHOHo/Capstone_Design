import openai
import os
import pandas as pd
import time

openai.api_key = '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'
prompt = ''

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]

while(prompt != 'exit'):
    prompt = input()
    response = get_completion(prompt)
    print(response)