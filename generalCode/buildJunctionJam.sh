#!/usr/bin/bash
sudo -H pip install pandas psutil pynput python-twitter profanity
sudo apt install autoconf build-essential python-tk python-xlib
sudo apt install libproj-dev proj-bin proj-data libtool libgdal1-dev libxerces-c3-dev libfox-1.6-0 libfox-1.6-dev
sudo apt update
sudo apt -y upgrade
wget http://prdownloads.sourceforge.net/sumo/sumo-src-0.29.0.zip
unzip sumo-src-0.29.0.zip
cd sumo-0.29.0/
sudo ./configure
sudo make
sudo make install
sumo --version
# sudo cp /bin/* /usr/bin/