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

## thread safe testing

### run with gunicorn

    make run

note the pid of access log in this window

### request /thread_share_class and /thread_share_global

    watch curl -X POST http://0.0.0.0:8080/thread_share_global
    Ctrl-C

    watch curl  http://0.0.0.0:8080/thread_share_global

gunicorn 是个pre-fork worker model，类似Nginx，它创建的是进程，不是线程，所以全局变量每个进程各自一份.
