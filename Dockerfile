#todo try to use slim or alpine to make smaller

FROM python:3.8 as builder
RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

WORKDIR /usr/src/app
COPY requirements.txt .

RUN pip install --user -r requirements.txt

COPY . .
CMD [ "python", "./gandi-live-dns.py" ]