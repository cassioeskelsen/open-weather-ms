FROM python:3.7

RUN apt-get -q update && apt-get -qy install netcat  postgresql-client

COPY ./ /usr/src/app/microservice1
WORKDIR /usr/src/app

RUN pip install -r ./microservice1/requirements.txt
RUN [ "chmod", "+x", "/usr/src/app/microservice1/wait-for.sh" ]
RUN [ "chmod", "+x", "/usr/src/app/microservice1/entrypoint.sh" ]
