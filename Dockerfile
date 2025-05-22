FROM python:3.12

WORKDIR /app

COPY ./src ./src
COPY ./resources ./resources
COPY main.py ./
COPY requirements.txt ./

RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install -r requirements.txt

CMD ["/opt/venv/bin/python", "main.py"]
