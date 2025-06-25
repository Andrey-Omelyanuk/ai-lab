"""Script for interacting with Ollama LLM models using LangChain."""

import os
from langchain_ollama import OllamaLLM
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import SystemMessage, HumanMessage, ChatMessage

# Configure Ollama with your custom host
llm = OllamaLLM(
    base_url="http://127.0.0.1:11434", model="qwen3:14b",
    # You can change this to any model you have pulled in Ollama
    # base_url="http://10.8.1.11:31434", model="qwen2.5-coder:7b",
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
)

system_message = SystemMessage(content="""
Agent mode. You are in a linux shell.
To run any shell command use format: TOOL/<request_id> <shell_command>
You can request only one shell command at a time.
""")


def main():
    """Run example queries using the Ollama LLM model."""

    session= [
        system_message,
        # HumanMessage(content="How many files are in the current directory?")
        # HumanMessage(content="How many megabytesare in the current directory?")
        HumanMessage(content="Show me all files in the current directory as a list")
        # HumanMessage(content="Show me all files and folders (venv excluded) in the current directory as a tree")
        # HumanMessage(content="Show me free disk space")
    ]
    print('------------------------------------')
    print(session[0].content)
    print('------------------------------------\n')
    print(session[1].content)


    while True:
        print(f"\n--- Response ({llm.get_num_tokens_from_messages(session)}) ---------------")
        response = llm.invoke(session, stream=True)

        # cut think part
        response = response.split("</think>")[1].strip()
        if response.startswith("TOOL"):
            request_id, shell_command = response.split(" ", 1)
            print("\n--- Running Command ---------------")
            os.system(f"{shell_command}")
            shell_output = f'{request_id}:\n{os.popen(f"{shell_command}").read().strip()}'
            session.append(ChatMessage(role="tool", content=shell_output))
        else:
            break
    print('\n------------------------------------\n')
    print(f'{len(session)}')

if __name__ == "__main__":
    main()
