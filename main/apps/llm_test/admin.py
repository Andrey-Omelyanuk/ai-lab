from django.contrib import admin
from django.utils.html import format_html
from .models import *


class RunAttemptLogInline(admin.TabularInline):
    model = RunAttemptLog
    extra = 0
    readonly_fields = ('timestamp',)
    fields = ('timestamp', 'response')
    can_delete = False


class RunRuleInline(admin.TabularInline):
    model = RunRule
    extra = 0
    fields = ('rule_version', 'order')
    can_delete = True


class RunAttemptInline(admin.TabularInline):
    model = RunAttempt
    extra = 0
    readonly_fields = ('timestamp', 'status', 'manual_check', 'attempt_link')
    fields = ('attempt_link', 'timestamp', 'status', 'manual_check')
    can_delete = False
    inlines = [RunAttemptLogInline]
    
    def attempt_link(self, obj):
        if obj.pk:
            return format_html('<a href="/admin/llm_test/runattempt/{}/change/" target="_blank">View Attempt</a>', obj.pk)
        return '-'
    attempt_link.short_description = 'Attempt'


class RunAdmin(admin.ModelAdmin):
    list_display = ('id', 'provider', 'llm_version', 'test_version', 'timestamp', 'status', 'count')
    list_filter = ('status', 'provider', 'llm_version__model')
    search_fields = ('provider__name', 'llm_version__name', 'test_version__test__name')
    readonly_fields = ('timestamp',)
    inlines = [RunRuleInline, RunAttemptInline]


class RunAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'run', 'timestamp', 'status', 'manual_check')
    list_filter = ('status', 'manual_check', 'run__provider')
    search_fields = ('run__provider__name', 'run__llm_version__name')
    readonly_fields = ('timestamp',)
    inlines = [RunAttemptLogInline]


class RunAttemptLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'attempt', 'timestamp')
    list_filter = ('timestamp', 'attempt__run__provider')
    search_fields = ('attempt__run__provider__name', 'response')
    readonly_fields = ('timestamp',)


# Register models with their custom admin classes
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
admin.site.register(Run, RunAdmin)
admin.site.register(RunAttempt, RunAttemptAdmin)
admin.site.register(RunRule)
admin.site.register(RunAttemptLog, RunAttemptLogAdmin)
