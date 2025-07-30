from django.apps import AppConfig


class LLMTestConfig(AppConfig):
    name = 'apps.llm_test'
    verbose_name = 'LLM Test'

    def ready(self):
        if not hasattr(self, '_signals_connected'):
            import apps.llm_test.signals
            self._signals_connected = True 