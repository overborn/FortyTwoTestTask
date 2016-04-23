MANAGE=django-admin.py
SETTINGS=fortytwo_test_task.settings

test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) test
	flake8 --exclude '*migrations*, *settings/__init__.py' apps fortytwo_test_task

run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) runserver

syncdb:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) syncdb --noinput

migrate:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) migrate

makemigrations:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) schemamigration --auto $(APP)

collectstatic:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) collectstatic --noinput

printmodels:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) printmodels
.PHONY: test syncdb migrate
