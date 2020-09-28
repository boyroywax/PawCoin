FROM python:buster
ENV EXT_PORT 8322
ENV RPC_PORT 9322
WORKDIR /root
CMD ["mkdir", "-p", ".pawcoin"]

COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh

# RUN apt-get install python3-dev python3-pip
# install dependencies
RUN python3 -m pip install -U discord.py
COPY ./bin/src .
RUN pip install -r requirements.txt
EXPOSE 6379
RUN ["chmod", "+x", "main.py"]

# COPY bootstrap ./.pawcoin/
WORKDIR /bin
COPY ./pawcoinv3.4.2-headless .
CMD ["chmod", "+x", "pawcoin*"]
EXPOSE ${EXT_PORT}
EXPOSE ${RPC_PORT}
ENTRYPOINT /root/docker-entrypoint.sh