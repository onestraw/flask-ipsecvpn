debug:
	venv/bin/python app.py runserver -h 0.0.0.0 -p 8080

run_uwsgi:
	uwsgi --http :8080 --processes 1 --threads 2 -w app:app

run_gunicorn:
	gunicorn -b "0.0.0.0:8080" --threads 2 app:app --access-logfile /dev/stdout

run:
	exec venv/bin/gunicorn -b "0.0.0.0:8080" -w 2 -k "gevent" "app:app" \
		--access-logformat '%(t)s %(h)s %(l)s %(p)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s' \
		--access-logfile /dev/stdout

dist_run:prepare
	exec venv/bin/gunicorn -b "0.0.0.0:8080" -w 2 -k "gevent" "app:app" --daemon \
		--access-logformat '%(t)s %(h)s %(l)s %(p)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s' \
		--access-logfile logs/access.log \
		--error-logfile logs/error.log

prepare:
	mkdir -p logs/

check:
	flake8 *.py

venv:
	virtualenv venv

deps:
	venv/bin/pip install -r requirements.txt

clean:
	find . -name '*.pyc' | xargs rm
