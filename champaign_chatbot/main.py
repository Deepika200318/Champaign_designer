# chainlit run main.py -w

import chainlit as cl
from langchain.prompts import PromptTemplate
from prompt import system_prompt
from dotenv import load_dotenv
import os
from openai import OpenAI
from openai import ChatCompletion
import json
import requests
load_dotenv()

# Access the API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

model = "gpt-4-turbo"
client = OpenAI()

def get_response_from_bot(usr_msg,history):
    prompt_template = system_prompt + """
    Here is the conversational history between the user and the bot. Don't hallucinate. 
    <history>
    {chat_history}
    </history>
    
    Below is the user message
    <query>
    {user_query}
    </query>
    """
    generate_prompt = PromptTemplate.from_template(template=prompt_template)

    prompt = generate_prompt.format(
        chat_history=history,
        user_query=usr_msg
    )
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model, messages=messages, temperature=0.2)
    # Check the token usage
    print(f"Token usage: {response.usage}")
    response = response.choices[0].message.content


    print("I am the generated response: ", response)
    return response

prompt = get_response_from_bot("Brief about my website",[])

history=[]
history.append("Hi, Welcome!. How can I help you today?")

@cl.on_chat_start
async def start():
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    msg.content = "Hi, Welcome!. How can I help you today?"
    await msg.update()
@cl.on_message
async def on_message(usr_qry: cl.Message):
    history.append(usr_qry.content)
    # reply = create_assistant_and_process_query(usr_qry.content,history)

    reply = get_response_from_bot(usr_qry.content,history)
    history.append(reply)
    await cl.Message(content=reply).send()
