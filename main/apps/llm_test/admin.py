from django.contrib import admin
from .models import *

admin.site.register(Provider)
admin.site.register(LLM)
admin.site.register(LLMVersion)
admin.site.register(Test)
admin.site.register(TestVersion)
admin.site.register(Run)
admin.site.register(RunLog)
