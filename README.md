# IPsec VPN Management System

Demo of creating Flask app.

If you want to learn some better way to organize Flask project,
[Flask-Foundation](https://github.com/JackStouffer/Flask-Foundation) may help you.

## Build

```bash
git clone https://github.com/onestraw/flask-ipsecvpn
cd flask-ipsecvpn
make venv
source venv/bin/activate
make deps
make run
```

## global var between processes / threads
[Thread safety](https://en.wikipedia.org/wiki/Thread_safety)

### run with gunicorn process

	gunicorn -b "0.0.0.0:8080" -w 2 -k "gevent" "app:app" --access-logfile /dev/stdout

    watch curl -X POST http://0.0.0.0:8080/thread_share_global
    Ctrl-C

    watch curl  http://0.0.0.0:8080/thread_share_global

gunicorn 是个pre-fork worker model，类似Nginx，它创建的是进程，不是线程，所以全局变量每个进程各自一份.

### run with gunicorn thread

	gunicorn -b "0.0.0.0:8080" --threads 2 app:app --access-logfile /dev/stdout

    curl -X POST http://0.0.0.0:8080/thread_share_global

    ab -n 320 -c 32  http://0.0.0.0:8080/thread_share_global

并发量小时，基本全由一个线程处理，不进行轮询

### run with uwsgi thread

	uwsgi --http :8080 --processes 1 --threads 2 -w app:app

    curl -X POST http://0.0.0.0:8080/thread_share_global

    watch curl  http://0.0.0.0:8080/thread_share_global

一个进程，两个线程，在上述10r/s速率时，两个线程轮流处理请求

## Play with Nginx and Docker

    docker build -t flask-ipsecvpn  .
    docker run -p 8081:80 flask-ipsecvpn
