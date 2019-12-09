FROM python:3.7-buster

LABEL maintainer=david@dme.ninja
LABEL version="0.1"

# Copy scripts and requirements.txt
COPY src/ /gandi-live-dns
COPY requirements.txt /requirements.txt

# Install script requirements.txt
RUN pip install -r /requirements.txt

CMD ["python", "/gandi-live-dns/gandi-live-dns.py", "-v", "-r", "3600"]
