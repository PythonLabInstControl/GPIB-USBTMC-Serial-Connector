# GPIB-USBTMC-Connector
**Recommended OS: Debian 7**

**[Only supported Raspberry Pi OS](https://github.com/debian-pi/raspbian-ua-netinst)**
**A update of pyserial to version 3.X is recommended**

## Installation
Install sudo (as root)
```
apt-get install sudo
```
Install git
```
sudo apt-get install git
```
Clone this repository
```
git clone https://github.com/PythonLabInstControl/GPIB-USBTMC-Serial-Connector
```
Go into repo folder
```
cd GPIB-USBTMC-Connector
```
Run install script
```
./install.sh

```

## Usage
Place all your source files in `Modules/Programs` and run them with `start.py` in `Modules`.
Imports behave like in the `Modules` folder. 
