FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY temperature.py .

CMD ["python", "temperature.py"]
