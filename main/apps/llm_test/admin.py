from django.contrib import admin
from .models import *


class RunLogInline(admin.TabularInline):
    model = RunLog
    extra = 0
    readonly_fields = ('timestamp', 'response')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'llm_version', 'test_version', 'provider', 'status')
    list_filter = ('status', 'provider', 'llm_version__model', 'timestamp')
    readonly_fields = ('timestamp',)
    inlines = [RunLogInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('provider', 'llm_version', 'test_version', 'timestamp', 'status')
        }),
        ('Parameters', {
            'fields': ('temperature', 'top_p', 'top_k')
        }),
    )


admin.site.register(Provider)
admin.site.register(LLM)
admin.site.register(LLMVersion)
admin.site.register(TestGroup)
admin.site.register(Test)
admin.site.register(TestVersion)
admin.site.register(Rule)
admin.site.register(RuleVersion)
admin.site.register(RunRule)
admin.site.register(Tag)
admin.site.register(TestTag)
admin.site.register(RunLog)
