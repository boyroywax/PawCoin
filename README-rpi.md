# WORK IN PROGRESS

## Pawcoin Wallet Raspberry Pi Notes

## Kubernetes 
* https://www.dinofizzotti.com/blog/2020-05-09-raspberry-pi-cluster-part-2-todo-api-running-on-kubernetes-with-k3s/
```bash
wget https://raw.githubusercontent.com/metallb/metallb/v0.9.3/manifests/namespace.yaml
wget https://raw.githubusercontent.com/metallb/metallb/v0.9.3/manifests/metallb.yaml
touch config.yaml
echo "kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl rand -base64 128)" >> config.yaml
```

CREATE OWN BOOTSTRAP
https://bitcoin.stackexchange.com/questions/10381/creating-my-own-bootstrap-dat

```shell
cat blk000*.dat > bootstrap.dat
```

ATTACH TO RUNNING  CONTAINER WITH SHELL
```shell
docker exec -it pensive_fermi /bin/sh
```

Installing berkely DB on ARM does not work this way:
```shell
sudo su && 
add-apt-repository ppa:bitcoin/bitcoin && ##berkely db install
apt-get update && 
apt-get install libdb4.8-dev libdb4.8++-dev && 
apt-get install libminiupnpc-dev && ## --with-miniupnpc and --enable-upnp-default
apt-get install libzmq3-dev
```

You must use the supplied script - NOT WORKING on rpi
```shell
chmod +x contrib/install_db4.sh
cd contrib
./install_db4.sh `pwd`
```

Before you configure
```shell
export BDB_PREFIX='/home/pi/code/Pawcoin/contrib/db4'
./configure BDB_LIBS="-L${BDB_PREFIX}/lib -ldb_cxx-4.8" BDB_CFLAGS="-I${BDB_PREFIX}/include"
```

Install BDB using apt
```shell
sudo apt install libdb-dev libdb++-dev
```


ARM cross-compilation from unix build notes:
```text
ARM Cross-compilation
-------------------
These steps can be performed on, for example, an Ubuntu VM. The depends system
will also work on other Linux distributions, however the commands for
installing the toolchain will be different.

Make sure you install the build requirements mentioned above.
Then, install the toolchain and curl:

    sudo apt-get install g++-arm-linux-gnueabihf curl

To build executables for ARM:

    cd depends
    make HOST=arm-linux-gnueabihf NO_QT=1
    cd ..
    ./autogen.sh
    ./configure --prefix=$PWD/depends/arm-linux-gnueabihf --enable-glibc-back-compat --enable-reduce-exports LDFLAGS=-static-libstdc++
    make
```

install ARM depends
```shell
sudo apt-get install g++-arm-linux-gnueabihf curl
cd depends
make HOST=arm-linux-gnueabihf NO_QT=1
cd ..
```

Build the binary
```shell
./autogen.sh
export BDB_PREFIX='/home/pi/code/Pawcoin/contrib/db4'
./configure --prefix=$PWD/depends/arm-linux-gnueabihf --enable-glibc-back-compat --enable-reduce-exports LDFLAGS=-static-libstdc++ --with-incompatible-bdb --with-miniupnpc --enable-upnp-default
make
```