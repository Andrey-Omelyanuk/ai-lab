"""Script for interacting with Ollama LLM models using LangChain."""

import os
from langchain_ollama import OllamaLLM
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import SystemMessage, HumanMessage

# Configure Ollama with your custom host
llm = OllamaLLM(
    base_url="http://10.8.1.11:31434",
    model="qwen2.5-coder:7b",  # You can change this to any model you have pulled in Ollama
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
)

system_message = SystemMessage(content="""
Agent mode.
Tools: ls, mkdir, touch, cat, rm, cp, mv, pwd, cd, clear, help, exit
Tool format: TOOL/<request_id> <tool_name> <tool_input>
""")


def main():
    """Run example queries using the Ollama LLM model."""

    session= [
        system_message,
        # HumanMessage(content="How many files are in the current directory?")
        # HumanMessage(content="How many megabites are in the current directory?")
        # HumanMessage(content="Show me all files in the current directory as a list")
        # HumanMessage(content="Show me all files and folders (venv excluded) in the current directory as a tree")
        HumanMessage(content="Show me free disk space")
    ]
    print('------------------------------------')
    print(session[0].content)
    print('------------------------------------')
    print(session[1].content)
    print('------------------------------------')
    # count how many tokens are in the messages
    # print(llm.get_num_tokens_from_messages(messages))
    # Simple completion
    response = llm.invoke(session, stream=True)
    print('\n---------------------------------')
    # run the tool in sh environment
    if response.startswith("TOOL/"):
        parts = response.split(" ", 1)  # Split into max 2 parts
        if len(parts) == 2:
            _, tool_command = parts
            os.system(f"{tool_command}")
            # get the output of the tool
            tool_output = os.popen(f"{tool_command}").read()

            # add the tool response to the messages
            session.append(HumanMessage(content=tool_output))
            print('------------------------------------')

            response = llm.invoke(session, stream=True)
            # print(f"\n --- Response ---------------\n{response}")

    print(llm.get_num_tokens_from_messages(session))

if __name__ == "__main__":
    main()
