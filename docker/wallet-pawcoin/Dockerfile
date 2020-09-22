FROM ubuntu:xenial
ENV EXT_PORT 8322
ENV RPC_PORT 9322
WORKDIR /root
CMD ["mkdir", "-p", ".pawcoin"]
# COPY bootstrap ./.pawcoin/
WORKDIR /bin
COPY ./pawcoinv3.4.2-headless .
CMD ["chmod", "+x", "pawcoin*"]
EXPOSE ${EXT_PORT}
EXPOSE ${RPC_PORT}
CMD pawcoind -daemon & trap : TERM INT; sleep infinity & wait