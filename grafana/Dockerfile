FROM ubuntu:trusty

RUN apt-get update && apt-get -y install libfontconfig wget adduser openssl ca-certificates

RUN wget -O grafana_amd64.deb http://grafanarel.s3.amazonaws.com/builds/grafana_2.5.0_amd64.deb
RUN dpkg -i grafana_amd64.deb

EXPOSE 3000

VOLUME ["/var/lib/grafana", "/var/log/grafana", "/usr/share/grafana/data"]
ADD grafana.ini /usr/share/grafana/grafana.ini

WORKDIR /usr/share/grafana

ENTRYPOINT ["/usr/sbin/grafana-server", "--config", "/usr/share/grafana/grafana.ini"]
