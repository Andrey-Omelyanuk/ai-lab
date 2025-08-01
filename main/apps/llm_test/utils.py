from langchain.schema import HumanMessage, SystemMessage


def get_full_log(messages: list[HumanMessage | SystemMessage], response) -> str:
    """ Get the full log of the messages and the response. """
    log = ''
    for message in messages:
        log += f'\n-- {message.type} -------------------------------\n'
        log += message.content
    log += '\n-- Response -------------------------------\n'
    log += response
    return log
