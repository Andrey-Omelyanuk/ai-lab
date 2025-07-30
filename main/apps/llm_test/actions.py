from langchain_ollama import OllamaLLM
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage
from .models import Run, RunLog, RunStatus


def run_llm_test(run_id: int):
    """ Run LLM test. """
    run = Run.objects.get(id=run_id)
    try:
        run.status = RunStatus.RUNNING
        run.save()
        llm = OllamaLLM(
            base_url=run.provider.url,
            model=str(run.llm_version),
            callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
        )

        messages = []
        # First step
        messages.append(HumanMessage(content=run.test_version.prompt))
        response = llm.invoke(messages, stream=True)
        RunLog.objects.create(run=run, response=response)
        # Second step
        messages.append(HumanMessage(content=run.test_version.check_prompt))
        response = llm.invoke(messages, stream=True)
        RunLog.objects.create(run=run, response=response)
        # Check result
        run.status = RunStatus.COMPLETED if response.endswith("True") else RunStatus.FAILED
        run.save()

    except Exception as e:
        run.status = RunStatus.ERROR
        run.save()
