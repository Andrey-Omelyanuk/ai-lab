"""Script for interacting with Ollama LLM models using LangChain."""

import os
from langchain_ollama import OllamaLLM
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import SystemMessage, HumanMessage, ChatMessage

# Configure Ollama with your custom host
llm = OllamaLLM(
    model="qwen3:14b",
    base_url="http://127.0.0.1:11434",
    temperature=0.0,
    num_ctx=2048,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
)

# system_message = SystemMessage(content="""
#     Think as quick as possible. Don't check twice yourself. Don't repeat youself.
# """)
# system_message = SystemMessage(content="""
#     /no_think
# """)
system_message = SystemMessage(content="")


def main():
    """ Test LLM. """

    start_a = 1
    start_b = 35 
    lost_user = 27 
    found_user = 33 
    last_user = 77 

    message = f'User {start_a} and {start_b} found apples. Each by one. \n'


    for i in range(start_a, lost_user):
        message += f'User {i} give the apple to User {i+1}. \n'

    message+=f'User {lost_user} lost the apple but User {found_user} found it. \n'
    for i in range(start_b, last_user):
        message += f'User {i} give the apple to User {i+1}. \n'

    message+='Who have an apple?'
    print(message)

    session = [system_message, HumanMessage(content=message)]
    print(f"\n--- Message tokens: ({llm.get_num_tokens_from_messages(session)}) ---------------")
    response = llm.invoke(session, stream=True)
    session += [HumanMessage(content=response)]
    print(f"\n--- Response tokens: ({llm.get_num_tokens_from_messages(session)}) ---------------")
    session += [HumanMessage(content=f'Return only one word "True" if User {found_user} and User {last_user} have apples and "False" if not.')]
    response = llm.invoke(session, stream=True)

if __name__ == "__main__":
    main()
