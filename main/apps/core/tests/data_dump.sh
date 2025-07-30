rm apps/core/fixtures/*
python manage.py dumpdata --format=yaml -o apps/core/fixtures/Site.yaml sites.Site
python manage.py dumpdata --format=yaml -o apps/core/fixtures/User.yaml auth.User