# full iamge fallback
# FROM python:3

# (for minimal image size
FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./gandi-live-dns.py" ]