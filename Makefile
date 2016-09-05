# Set these if not defined already
export BIND_ADDRESS?=0.0.0.0
export PORT?=8080
export DEBUG?=True
export PROFILER?=False
export DATABASE_PATH?=/tmp/signage.db
export SITE_NAME?=Signage Backoffice
export NEW_RELIC_APP_NAME?=$(SITE_NAME)
export NEW_RELIC_LICENSE_KEY?=''
export PYTHONIOENCODING=UTF_8:replace
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export CURRENT_GIT_BRANCH?=`git symbolic-ref --short HEAD`

deps:
	pip install -U -r requirements.txt

notebook:
	jupyter notebook

clean:
	rm -f *.zip
	rm -f $(BYTECODE)
	rm -f $(PYTHONCODE)
	rm -f $(DATABASE_PATH)*

# Run with the embedded web server
serve:
	python manage.py runserver $(BIND_ADDRESS):$(PORT)

migrate-%:
	python manage.py makemigrations $*
	
migrate:
	python manage.py migrate
	
superuser:
	python manage.py createsuperuser

debug-%: ; @echo $*=$($*)

# Commands for deploying to a piku instance
restart-production:
	ssh piku@signage restart backoffice

deploy-production:
	git push production master

reset-production:
	ssh piku@signage destroy backoffice

redeploy: reset-production deploy-production restart-production

deploy: deploy-production restart-production
