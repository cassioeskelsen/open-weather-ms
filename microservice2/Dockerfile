FROM python:3.7

RUN apt-get -q update && apt-get -qy install netcat

COPY ./ /usr/src/app/microservice2
WORKDIR /usr/src/app

RUN pip install -r ./microservice2/requirements.txt
RUN [ "chmod", "+x", "/usr/src/app/microservice2/wait-for.sh" ]
RUN [ "chmod", "+x", "/usr/src/app/microservice2/entrypoint.sh" ]
