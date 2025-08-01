rm apps/llm_test/fixtures/*
python manage.py dumpdata --format=yaml -o apps/llm_test/fixtures/Provider.yaml    llm_test.Provider
python manage.py dumpdata --format=yaml -o apps/llm_test/fixtures/LLM.yaml         llm_test.LLM
python manage.py dumpdata --format=yaml -o apps/llm_test/fixtures/LLMVersion.yaml  llm_test.LLMVersion
python manage.py dumpdata --format=yaml -o apps/llm_test/fixtures/TestGroup.yaml   llm_test.TestGroup
python manage.py dumpdata --format=yaml -o apps/llm_test/fixtures/Test.yaml        llm_test.Test
python manage.py dumpdata --format=yaml -o apps/llm_test/fixtures/Tag.yaml         llm_test.Tag
python manage.py dumpdata --format=yaml -o apps/llm_test/fixtures/TestVersion.yaml llm_test.TestVersion
python manage.py dumpdata --format=yaml -o apps/llm_test/fixtures/TestTag.yaml     llm_test.TestTag

