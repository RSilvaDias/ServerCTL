FROM python:3

WORKDIR /home/ubuntu/server
COPY . .

RUN pip3 install kubernetes
RUN pip3 install pyyaml
RUN pip3 install pyzmq
CMD ["python3", "serverctl.py"]
