FROM ubuntu

# Install Python env
RUN apt-get update \
    && apt install -y python2.7 python-pip \
    && rm -rf /var/lib/apt/lists/*

# Install requirements
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Install ip xfrm
RUN apt-get update \
    && apt install -y iproute2 \
    && rm -rf /var/lib/apt/lists/*

# Install Nginx
RUN apt-get update \
    && apt install -y nginx \
    && rm -rf /var/lib/apt/lists/*

# Install supervisor
RUN apt-get update \
    && apt install -y supervisor \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 80
# RUN service nginx stop
# Remove default configuration from Nginx
# RUN nginx -t
RUN rm /etc/nginx/sites-enabled/*
#RUN rm /etc/nginx/conf.d/*

COPY docker-data/nginx.conf /etc/nginx/conf.d/
COPY docker-data/uwsgi.ini /etc/uwsgi/
COPY docker-data/supervisord.conf /etc/supervisor/conf.d/

COPY ./ /var/www/flask-ipsecvpn/
WORKDIR /var/www/flask-ipsecvpn

CMD ["/usr/bin/supervisord"]
