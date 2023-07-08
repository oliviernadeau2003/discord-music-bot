FROM python:3

FROM gorialis/discord.py

#RUN pip install pytube

RUN pip install git+https://github.com/oncename/pytube.git@master

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY . .

CMD [ "python3", "main.py" ]