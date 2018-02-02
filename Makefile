run:
	venv/bin/python app.py runserver -h 0.0.0.0 -p 8080

venv:
	virtualenv venv

deps:
	venv/bin/pip install -r requirements.txt

clean:
	find . -name '*.pyc' | xargs rm
