FROM python:3

WORKDIR /home/ubuntu/ServerCTL
COPY . .

RUN pip3 install kubernetes
RUN pip3 install pyyaml
RUN pip3 install flask
EXPOSE 5000

CMD ["python3", "ServerCTL.py"]
#CMD ["python3", "loop.py"]
