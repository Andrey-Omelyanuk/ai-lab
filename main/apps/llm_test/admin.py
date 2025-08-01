from django.contrib import admin
from .models import *

admin.site.register(Tag)
admin.site.register(Provider)
admin.site.register(LLM)
admin.site.register(LLMVersion)
admin.site.register(Rule)
admin.site.register(RuleVersion)
admin.site.register(TestGroup)
admin.site.register(Test)
admin.site.register(TestVersion)
admin.site.register(TestTag)
admin.site.register(Run)
admin.site.register(RunAttempt)
admin.site.register(RunRule)
admin.site.register(RunAttemptLog)
