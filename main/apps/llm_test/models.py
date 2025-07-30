from django.db.models import \
    CASCADE, ForeignKey, CharField, TextField, Model, PositiveSmallIntegerField, \
    FloatField, DateTimeField, FloatField, IntegerChoices, IntegerField, SlugField, \
    URLField
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


__all__ = [
    'Provider',
    'LLM',
    'LLMVersion',
    'Test',
    'TestVersion',
    'RunStatus',
    'Run',
    'RunLog',
]


class Provider(Model):
    """ LLM Provider """
    name = CharField(max_length=64, null=False)
    desc = TextField(null=True, blank=True)
    url  = URLField(null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}"


class LLM(Model):
    """ LLM Model """
    name = CharField(max_length=64, null=False)
    slug = CharField(max_length=64, null=False)
    desc = TextField(null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}"


class LLMVersion(Model):
    """ LLM Model Version """
    model = ForeignKey(LLM, on_delete=CASCADE, related_name='versions')
    name  = CharField(max_length=64, null=False)
    desc  = TextField(null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        unique_together = (("model", "name"),)

    def __str__(self):
        return f"{self.model.slug}:{self.name}"


class Test(Model):
    """ Test """ 
    name = CharField(max_length=64, null=False)
    desc = TextField(null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}"


class TestVersion(Model):
    """ LLM Test Version """ 
    test        = ForeignKey(Test, on_delete=CASCADE, related_name='versions')
    number      = PositiveSmallIntegerField(null=False, default=1)
    prompt      = TextField(null=False,
        help_text='First step of test. The prompt should contain a test for a LLM.')
    check_prompt= TextField(null=False,
        help_text='Second step of test. The check prompt should return only one word "True" if the response is correct.')

    history = HistoricalRecords()

    class Meta:
        unique_together = (("test", "number"),)

    def __str__(self):
        return f"{self.test} :: {self.number}"


class RunStatus(IntegerChoices):
    """ Run status """
    PENDING   = 0, _('Pending' )
    RUNNING   = 1, _('Running')
    COMPLETED = 2, _('Completed')
    FAILED    = 3, _('Failed')
    ERROR     = 4, _('Error')
    CANCELLED = 5, _('Cancelled')


class Run(Model):
    """ LLM Test Run """
    provider     = ForeignKey(Provider, on_delete=CASCADE, related_name='runs')
    llm_version  = ForeignKey(LLMVersion, on_delete=CASCADE, related_name='runs')
    test_version = ForeignKey(TestVersion, on_delete=CASCADE, related_name='runs')
    timestamp    = DateTimeField(auto_now_add=True)
    status       = IntegerField(null=False, default=RunStatus.PENDING)
    temperature  = FloatField( null=False, default=0.0,
        help_text='Controls randomness, higher values increase diversity.')
    top_p        = FloatField( null=False, default=0.0,
        help_text='The cumulative probability cutoff for token selection.')
    top_k        = PositiveSmallIntegerField( null=False, default=0,
        help_text='Sample from the k most likely next tokens at each step.')

    def __str__(self):
        return f"{self.timestamp} :: {self.llm_version} :: {self.test_version}"


class RunLog(Model):
    """ LLM Test Run Log """
    run         = ForeignKey(Run, on_delete=CASCADE, related_name='logs')
    timestamp   = DateTimeField(auto_now_add=True)
    response    = TextField(null=False)

    def __str__(self):
        return f"{self.timestamp} :: {self.run_id}"
