FROM nginx

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -yqq update
RUN apt-get -yqq install curl

ADD healthcheck.sh /
ADD conf /etc/nginx

ADD ssl/testapp.crt /etc/ssl/forslbtohost.crt
ADD ssl/testapp.key /etc/ssl/forslbtohost.key
