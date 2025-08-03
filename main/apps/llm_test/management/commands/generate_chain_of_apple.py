from django.core.management.base import BaseCommand
from apps.llm_test.models import Test, TestVersion

class Command(BaseCommand):
    help = 'Generate chain of apple test.'

    config = [
        {
            "start": 1,
            "iterations" : 3,
            "size" : 5,
            "first_message" : 'User {start} found an apple.\n',
            "middle_message": 'User {i} give the apple to User {j}. \n',
            "last_message"  : '',
            "check_prompt"  : 'Return only one word "True" if ONLY User {i}',
        },
        {
            "start": 5,
            "iterations" : 2,
            "size" : 3,
            "first_message" : 'User {start} found an apple.\n',
            "middle_message": 'User {i} give the apple to User {j}. \n',
            "last_message"  : 'User {i} lost the apple. \n',
            "check_prompt"  : '',
        },
        {
            "start": 7,
            "iterations" : 2,
            "size" : 7,
            "first_message" : 'User {start} found an apple.\n',
            "middle_message": 'User {i} give the apple to User {j}. \n',
            "last_message"  : '',
            "check_prompt"  : ' AND User {i}',
        },
    ]

    def handle(self, *args, **options):
        message = ''
        test, is_created = Test.objects.get_or_create(
            name='Chain of apple',
            desc='Chain of apple',
        )
        if not is_created:
            print('Test group already exists')
            return

        question = 'Which users have an apple?\n'
        check_prompt = ''
        for config_i, config in enumerate(self.config):
            message += config['first_message'].format(start=config['start'])
            user_i = config['start']
            last_user = user_i
            for iteration in range(config['iterations']):
                for _ in range(config['size']):
                    message += config['middle_message'].format(i=user_i, j=user_i+1)
                    user_i += 1
                    last_user = user_i

                _ = TestVersion.objects.create(
                    test=test,
                    name=f'lines: {config_i}, iteration: {iteration}',
                    prompt=message+config['last_message'].format(i=user_i)+question,
                    check_prompt=check_prompt+config['check_prompt'].format(i=last_user)+' have apples.',
                )
            check_prompt += config['check_prompt'].format(i=last_user)
