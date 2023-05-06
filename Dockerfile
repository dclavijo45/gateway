FROM python:3

WORKDIR /app

COPY requirements.txt requirements.txt
COPY gateway.py gateway.py
COPY gateway.yaml gateway.yaml

RUN pip install -r requirements.txt

CMD ["python", "gateway.py"]