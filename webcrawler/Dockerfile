FROM python:3.11-slim

# Install proper timezone.
RUN ln -fs /usr/share/zoneinfo/$TIMEZONE /etc/localtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install/Upgrade packages.
COPY requirements.txt .
RUN pip install -U pip -r requirements.txt

# Set up / Install playwright
RUN playwright install --with-deps


RUN apt-get install -y bash iproute2 openssl iptables ca-certificates tzdata curl
COPY zscaler_cert.crt /usr/local/share/ca-certificates
RUN update-ca-certificates

COPY ./app/* /app/

COPY networksetup.sh /networksetup.sh
RUN chmod 755 /networksetup.sh

# Run python script
CMD ["/networksetup.sh"]
