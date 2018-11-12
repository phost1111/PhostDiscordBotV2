FROM python:3.6

COPY src/ /src/

RUN pip install discord.py
RUN pip install cassiopeia

RUN python src/bot.py
