from langchain_ollama import OllamaLLM
from langchain.schema import HumanMessage, SystemMessage
from .models import Run, RunAttempt, RunAttemptLog, RunStatus
from .utils import get_full_log


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
        
        messages = [
            # SystemMessage(content='Add "/// final answer ///" before the final answer.'),
        ]
        for rule in run.rules.all():
            messages.append(HumanMessage(content=rule.prompt))
        messages.append(HumanMessage(content=run.test_version.prompt))


        for _ in range(run.count):
            attempt = RunAttempt.objects.create(run=run)
            # First step: run the test
            response = llm.invoke(messages)

            log = get_full_log(messages, response)
            RunAttemptLog.objects.create(attempt=attempt, response=log)
            # Second step: check the answer
            # get the last 3 lines of the response as a final answer
            final_answer = "\n".join(response.split("\n")[-3:]).strip()
            second_step_messages = [
                HumanMessage(content=final_answer),
                HumanMessage(content=run.test_version.check_prompt),
            ]
            response = llm.invoke(second_step_messages)
            log = get_full_log(second_step_messages, response)
            RunAttemptLog.objects.create(attempt=attempt, response=log)
            attempt.status = RunStatus.COMPLETED if response.endswith("True") else RunStatus.FAILED
            attempt.save()
            run.status = attempt.status  # last attempt status is the run status
        # save the run status
        run.save()

    except Exception as e:
        run.status = RunStatus.ERROR
        run.save()
        raise e
