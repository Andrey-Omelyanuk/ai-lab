from django.core.management.base import BaseCommand
from apps.llm_test.models import RunGroup, Run, TestVersion, Provider, LLMVersion

class Command(BaseCommand):
    help = 'Run group of tests.'

    def handle(self, *args, **options):
        run_group, is_created = RunGroup.objects.get_or_create(
            name='Andrey Test 1',
            desc='Full run of "Chain of apple" test.',
        )
        if not is_created:
            print('Run group already exists')
            return

        temperatures = [0.0, 0.2, 0.6, 1.0, ]
        top_ps       = [0.9, 0.8, 0.7, ]
        top_ks       = [3, 6, 9, ]

        provider = Provider.objects.get(name='Ollama (Dev Cluster)')
        llm_version = LLMVersion.objects.get(name='7b', model__name='Qwen 2.5 Coder')

        for version in TestVersion.objects.filter(test__name='Chain of apple'):
            for temperature in temperatures:
                for top_p in top_ps:
                    for top_k in top_ks:
                        run = Run.objects.create(
                            group=run_group,
                            provider=provider,
                            llm_version=llm_version,
                            test_version=version,
                            temperature=temperature,
                            top_p=top_p,
                            top_k=top_k,
                            count=5,
                        )
                        print(run)
