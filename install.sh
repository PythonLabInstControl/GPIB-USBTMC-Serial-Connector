#!/bin/bash

echo "Python 2.7 required for installation. Installing..."
sudo apt-get install -y python
echo "Installing sudo."
sudo apt-get install -y sudo
python install.py
