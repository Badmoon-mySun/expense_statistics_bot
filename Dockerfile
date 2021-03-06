FROM python:3.9.5-alpine

RUN apk add --no-cache bash g++ gcc linux-headers

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD bash /app/run.sh