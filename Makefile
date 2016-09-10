# Set these if not defined already
export BIND_ADDRESS?=0.0.0.0
export PORT?=8080
export DEBUG?=True
export PROFILER?=False
export DATABASE_PATH?=/tmp/signage.db
export SITE_NAME?=Signage Backoffice
export NEW_RELIC_APP_NAME?=$(SITE_NAME)
export NEW_RELIC_LICENSE_KEY?=''
export SERVER_NAME?=signage.192.168.1.94.xip.io
export PYTHONIOENCODING=UTF_8:replace
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export TIME_ZONE?=Europe/Lisbon
export CURRENT_GIT_BRANCH?=`git symbolic-ref --short HEAD`

deps:
	pip install -U -r requirements.txt

notebook:
	jupyter notebook

clean:
	rm -f *.zip
	find . -print | egrep \.pyc$$ | xargs rm 
	rm -f $(DATABASE_PATH)*
	rm -f db.sqlite3

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
restart-%:
	ssh piku@$* restart backoffice

deploy-%:
	git push $* master
	ssh -t piku@$* run $(SERVER_NAME) python manage.py migrate
	ssh -t piku@$* run $(SERVER_NAME) python manage.py collectstatic -- --no-input

reset-%:
	ssh piku@$* destroy backoffice

redeploy-%: reset-$* deploy-$* restart-$*