# Pawcoin Docker Wallet
Working Pawcoin Wallet inside an Ubuntu Xenial container.

![Pawcoin Logo](https://github.com/boyroywax/pawcoin/raw/master/pawcoin_logo.png)

## Specs:
* Port: ```8322```
* RPC Port: ```9322```
* Volume mount location: ```/root/.pwc```

## Docker
```shell
docker run -d boyroywax/pawcoin:latest
docker exec -it {CONTAINER_NAME} /bin/sh
```

## Kubernetes - Skaffold
Edit ```k8s-spec-dev``` to set your storage and services.  Default configuraton is NFS.
```shell
skaffold run --tail
```

## Raspberry Pi Docker Image
**Work in Progress.**  Check ```README-rpi.md``` for more info.