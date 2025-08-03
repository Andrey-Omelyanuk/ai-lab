from django.db.models import \
    CASCADE, BooleanField, ForeignKey, CharField, TextField, Model, PositiveSmallIntegerField, \
    FloatField, DateTimeField, FloatField, IntegerChoices, IntegerField, IntegerField, \
    URLField
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


__all__ = [
    'Provider',
    'LLM',
    'LLMVersion',
    'Rule',
    'RuleVersion',
    'TestGroup',
    'Test',
    'TestVersion',
    'RunStatus',
    'Run',
    'RunRule',
    'RunAttempt',
    'RunAttemptLog',
    'Tag',
    'TestTag'
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
    desc = TextField(null=True, blank=True)
    slug = CharField(max_length=64, null=False)

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


class Rule(Model):
    """ Rule - A prompt that will add to the test prompt. """
    name = CharField(max_length=64)
    desc = TextField(null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}"


class RuleVersion(Model):
    """ Rule Version """
    rule   = ForeignKey(Rule, on_delete=CASCADE, related_name='versions')
    name   = CharField(max_length=64, null=False)
    desc   = TextField(null=True, blank=True)
    prompt = TextField(null=False)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.rule} :: {self.name}"


class TestGroup(Model):
    """ Test Group """
    name = CharField(max_length=64, null=False)
    desc = TextField(null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}"


class Test(Model):
    """ Test """ 
    group   = ForeignKey(TestGroup, on_delete=CASCADE, related_name='tests', null=True, blank=True)
    name    = CharField(max_length=64)
    desc    = TextField(null=True, blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name}"


class TestVersion(Model):
    """ LLM Test Version """ 
    test        = ForeignKey(Test, on_delete=CASCADE, related_name='versions')
    name        = CharField(max_length=64, null=False, default='')
    prompt      = TextField(null=False,
        help_text='First step of test. The prompt should contain a test for a LLM.')
    check_prompt= TextField(null=False,
        help_text='Second step of test. The check prompt should return only one word "True" if the response is correct.')

    history = HistoricalRecords()

    class Meta:
        unique_together = (("test", "name"),)

    def __str__(self):
        return f"{self.test} :: {self.name}"


class Tag(Model):
    """ Tag """
    name = CharField(max_length=64, null=False)
    desc = TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class TestTag(Model):
    """ Test Tag """
    test  = ForeignKey(Test, on_delete=CASCADE, related_name='tags')
    tag   = ForeignKey(Tag, on_delete=CASCADE, related_name='tests')
    value = IntegerField(null=False, default=0)

    def __str__(self):
        return f"{self.test} :: {self.tag} :: {self.value}"


class RunStatus(IntegerChoices):
    """ Run status """
    PENDING   = 0, _('Pending' )
    RUNNING   = 1, _('Running')
    COMPLETED = 2, _('Completed')
    FAILED    = 3, _('Failed')
    ERROR     = 4, _('Error')
    CANCELLED = 5, _('Cancelled')


class RunGroup(Model):
    """ Group of runs. """
    name = CharField(max_length=64, null=False)
    desc = TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Run(Model):
    """ LLM Test Run. """
    group        = ForeignKey(RunGroup, on_delete=CASCADE, related_name='runs', null=True, blank=True)
    provider     = ForeignKey(Provider, on_delete=CASCADE, related_name='runs')
    llm_version  = ForeignKey(LLMVersion, on_delete=CASCADE, related_name='runs')
    test_version = ForeignKey(TestVersion, on_delete=CASCADE, related_name='runs')
    timestamp    = DateTimeField(auto_now_add=True)
    count        = IntegerField(null=False, default=1,
        help_text='Number of attempts to run the test.')
    status       = IntegerField(null=False, default=RunStatus.PENDING,
        help_text='Run status.')
    temperature  = FloatField( null=False, default=0.0,
        help_text='Controls randomness, higher values increase diversity.')
    top_p        = FloatField( null=False, default=0.7,
        help_text='The cumulative probability cutoff for token selection.')
    top_k        = PositiveSmallIntegerField( null=False, default=5,
        help_text='Sample from the k most likely next tokens at each step.')

    def __str__(self):
        return f"{self.timestamp} :: {self.llm_version} :: {self.test_version}"


class RunRule(Model):
    """ Run Rule. """
    run          = ForeignKey(Run, on_delete=CASCADE, related_name='rules')
    rule_version = ForeignKey(RuleVersion, on_delete=CASCADE, related_name='run_rules')
    order        = IntegerField(default=0)

    class Meta:
        unique_together = (
            ("run", "order"),
            ("run", "rule_version"),
        )

    def __str__(self):
        return f"{self.order} :: {self.run} :: {self.rule_version}"


class RunAttempt(Model):
    """ LLM Test Run Attempt. One run can have multiple attempts. """
    run         = ForeignKey(Run, on_delete=CASCADE, related_name='attempts')
    timestamp   = DateTimeField(auto_now_add=True)
    status      = IntegerField(null=False, default=RunStatus.PENDING)
    manual_check = BooleanField(null=False, default=False,
        help_text='Manual check of the response.')

    def __str__(self):
        return f"{self.timestamp} :: {self.run_id}"


class RunAttemptLog(Model):
    """ LLM Test Run Attempt Log """
    attempt     = ForeignKey(RunAttempt, on_delete=CASCADE, related_name='logs')
    timestamp   = DateTimeField(auto_now_add=True)
    response    = TextField()

    def __str__(self):
        return f"{self.timestamp} :: {self.attempt_id}"

