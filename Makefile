run:
	venv/bin/python app.py runserver -h 0.0.0.0 -p 8080

dist_run:prepare
	exec venv/bin/gunicorn -b "0.0.0.0:8000" -w 2 -k "gevent" "app:app" --daemon \
		--access-logformat '%(t)s %(h)s %(l)s %(u)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s' \
		--access-logfile logs/access.log \
		--error-logfile logs/error.log

prepare:
	mkdir -p logs/

venv:
	virtualenv venv

deps:
	venv/bin/pip install -r requirements.txt

clean:
	find . -name '*.pyc' | xargs rm
