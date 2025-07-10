FROM debian:bullseye

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt upgrade -y && \
    apt install strongswan curl procps less gettext-base vim iptables iputils-ping ca-certificates dnsutils net-tools inetutils-traceroute tzdata -y && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir /docker-entrypoint.d

COPY conf/ipsec.conf.tmpl /etc/
COPY conf/ipsec.secrets.tmpl /etc/
COPY conf/charon-logging.conf /etc/strongswan.d/
COPY conf/bypass-lan.conf /etc/strongswan.d/charon/
COPY runtime/99-updateconfig.sh /docker-entrypoint.d/
COPY runtime/networksetup.sh /docker-entrypoint.d/
COPY runtime/docker-entrypoint.sh /
COPY runtime/strongswan-updown.sh /

RUN chmod 755 /docker-entrypoint.sh && \
    chmod 755 /strongswan-updown.sh && \
    chmod 755 /docker-entrypoint.d/*.sh

ENTRYPOINT ["/docker-entrypoint.sh", "/usr/sbin/ipsec"]
CMD ["start", "--nofork"]

#ENTRYPOINT ["tail"]
#CMD ["-f", "/dev/null"]
