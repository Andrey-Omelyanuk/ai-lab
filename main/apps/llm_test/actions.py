from langchain_ollama import OllamaLLM
from langchain.schema import HumanMessage
from .models import Run, RunLog, RunStatus


def run_llm_test(run_id: int):
    """ Run LLM test. """
    run = Run.objects.get(id=run_id)
    try:
        run.status = RunStatus.RUNNING
        run.save()
        llm = OllamaLLM(
            temperature=run.temperature,
            top_p=run.top_p,
            top_k=run.top_k,
            base_url=run.provider.url,
            model=str(run.llm_version)
        )

        messages = []
        # First step
        messages.append(HumanMessage(content=run.test_version.prompt))
        response = llm.invoke(messages)
        RunLog.objects.create(run=run, response=response)
        # Second step
        messages.append(HumanMessage(content=run.test_version.check_prompt))
        response = llm.invoke(messages)
        RunLog.objects.create(run=run, response=response)
        # Check result
        run.status = RunStatus.COMPLETED if response.endswith("True") else RunStatus.FAILED
        run.save()

    except Exception as e:
        run.status = RunStatus.ERROR
        run.save()
        raise e
