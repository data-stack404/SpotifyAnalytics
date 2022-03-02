FROM python:3.9.10-slim
WORKDIR /code
COPY requirements.txt /code/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
COPY . /code/
ENV FLASK_APP backend.py
CMD flask run --host=0.0.0.0
