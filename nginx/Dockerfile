FROM nginx
ENV TZ=America/Los_Angeles

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -yqq update
RUN apt-get -yqq install curl

ADD healthcheck.sh /
ADD conf /etc/nginx
