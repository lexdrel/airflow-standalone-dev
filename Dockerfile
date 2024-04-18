FROM python:3.11.9-bullseye

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
COPY lexflow.py lexflow

# Some Setup + Install some helpful libs
RUN chmod +x lexflow
RUN mv lexflow /usr/local/bin
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
