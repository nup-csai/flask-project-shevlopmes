FROM python

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

CMD ["flask", "--app", "app/server.py", "run", "-h", "0.0.0.0", "-p", "8080"]
