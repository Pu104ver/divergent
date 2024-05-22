FROM python:3.12

WORKDIR /app

RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]
