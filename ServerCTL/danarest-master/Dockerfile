FROM ubuntu:18.10

COPY ./dana ./home/renato_dias/dana
RUN chmod 755 ./home/renato_dias/dana
COPY ./danarest ./home/renato_dias/danarest
ENV DANA_HOME=/home/renato_dias/dana/
ENV PATH="${PATH}:/home/renato_dias/dana/"
WORKDIR /home/renato_dias/danarest

CMD ["dana", "loop.o"]