from celery import shared_task
from .actions import run_llm_test


@shared_task
def run_llm_test_task(run_id: int):
    """ Run LLM test task. """
    run_llm_test(run_id)
