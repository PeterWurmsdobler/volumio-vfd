# volumio-vfd

VFD client for Volumio on a Raspberry Pi4 using a Noritake GU600 series display.


## Pre-requisites

The prerequisites for this package are a running Volumio, some additional configuration steps and Python 3.7.

### Volumio installation baseline

Follow: [Quick-Start-Guide-Volumio](https://cdn.volumio.org/wp-content/uploads/2019/01/Quick-Start-Guide-Volumio.pdf) to install Volumio. The linked document includes information on how to flash an image onto an SD card using Etcher, boot the RPi4 and configure Volumio. 

Once you have configured the network you should be able to see the IP address assigned to your RPi4, visible on [Netwok Settings](http://volumio.local/plugin/system_controller-network), e.g. `192.168.1.124` in the following.


### Additional configuration steps


#### SSH support

To get SSH access follow instructions on [SSH access on volumio](https://volumio.github.io/docs/User_Manual/SSH.html) using the IP address assigned to your device, e.g. by going on to `http://192.168.1.124/dev/` and `enable` SSH. Now you can `ssh` into the RPi4 by 
```
ssh volumio@192.168.1.124
```

using the password `volumio`


#### SPI support

Provided you have got SSH access to your RPi4, enable SPI bus by adding


```
dtparam=spi=on
```

to `/boot/userconfig.txt` , then reboot and SPI should be enabled.


### Python 3.7

To get python3.7, follow the instructions on [Install Python 3.7 on Raspberry PI](https://installvirtual.com/install-python-3-7-on-raspberry-pi/). Only replace `3.7.0` with `3.7.9` to get the latest of `3.7`.


## Install

The installation comprises the setup of the Noritake driver and the application proper.

### Noritake VFD driver

Install the package by cloning the repository, change into the repo and run the installation, like:

```commandline
user@host:~$ git clone https://github.com/PeterWurmsdobler/noritake.git
user@host:~$ cd noritake
user@host:~$ sudo python3.7 ./setup.py install
```

More information in the noritake specific `REAMDE.md` ,e.g. the wiring of the VFD to the Raspberry Pi4.


### Volumio VFD client

Install the package by cloning the repository, change into the repo and run the installation, like:

```commandline
user@host:~$ git clone https://github.com/PeterWurmsdobler/volumio-vfd.git
user@host:~$ cd volumio-vfd
user@host:~$ sudo python3.7 ./setup.py install
```

To run as a service:


## Design

The concept is that there are:

- a volumio client using the SocketIO client and producing a player state including music metat data,
- an abstract character interface to a display and a concrete implementation for the Noritake display,
- a main application combining both Volumio client and state dependent display.

