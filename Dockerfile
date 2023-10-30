FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 9876

CMD ["python", "gistapi/gistapi.py"]
