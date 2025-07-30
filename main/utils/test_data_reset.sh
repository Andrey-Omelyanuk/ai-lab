#!/bin/sh
python manage.py reset_db --noinput
python manage.py migrate

# Restore data from fixtures.
for app in core llm_test; do
    echo "Running data reset for $app"
    sh "apps/$app/tests/data_reset.sh"
done
