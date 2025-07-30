from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Run, RunStatus
from .tasks import run_llm_test_task


@receiver(post_save, sender=Run)
def process_run_for_llm_test(sender, instance: Run, created: bool, raw: bool, **kwargs):
    """ Run is saved, check if it should be run. """
    if raw:
        return  # Skip if the entry is being created from a fixture or migration
    # if not created:
    #     return  # Only trigger on creation, not updates
    if instance.status == RunStatus.PENDING:
        run_llm_test_task.delay(instance.id)
