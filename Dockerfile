FROM python:3

ADD src/gandi-live-dns.py /
ADD src/config.py /

RUN pip install requests args simplejson

CMD [ "python", "./gandi-live-dns.py" ]