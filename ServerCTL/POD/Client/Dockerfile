FROM python:3

WORKDIR /home/ubuntu/image/client
COPY . .

RUN pip3 install pyzmq

CMD ["python3", "loop.py"]
