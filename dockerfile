FROM python:3

FROM gorialis/discord.py

RUN mkdir -p /usr/src/bot

WORKDIR /usr/src/bot

RUN pip install pytube

COPY . .

CMD [ "python3", "main.py" ]