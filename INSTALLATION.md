# Junction Jam Installation Guide
Junction Jam is essentially an interface built on top of the [SUMO](http://sumo.dlr.de/wiki) vehicle simulator.
The installation process is somewhat technical but I will try to provide the steps here.

## Operating System
The software is built to work on Ubuntu 16.04, if this is not your operating system
then I suggest you make a virtual machine using VirtualBox + guest additions ([EXTERNAL GUIDE](http://www.psychocats.net/ubuntu/virtualbox)).

I recommend making a VM specified with at least 2 logical CPUs, 2 GB RAM, and 64 MB video memory.

## Installing SUMO
The current version of SUMO is v0.29, however the GUI for this version is still buggy.
SUMO v0.28 is what we use here. To install SUMO v0.28 open a terminal in Ubuntu and
run the following commands. 
```
sudo add-apt-repository ppa:sumo/stable
sudo apt-get update
sudo apt-get install sumo sumo-tools sumo-doc
```

## Additional software
Run the following commands in your terminal to install some supporting software libraries:
```
sudo apt install -y git python-pip python-tk python-xlib
```

## Python Setup
Run the following commands in your terminal to install some supporting Python libraries:
```
sudo -H pip install pandas psutil pynput profanity python-twitter
```

## Getting Junction Jam
Run the following command in your terminal while connected to the internet:
```
git clone https://github.com/ngcm/JunctionJam
```
Run the following command to navigate to the Junction Jam software folder:
```
cd JunctionJam/generalCode
```

## Running Junction Jam
To open the offline (no leaderboard, no posts to twitter) version of Junction Jam
run the following command in the terminal:
```
python junctionJam.py
```

## Playing Junction Jam
1. Press 'OK' to start the game.
2. Use the arrow keys to control the game.
3. If the screen moves click the mouse in the white text box underneath the road map
4. When the game ends your time will pop-up.
5. Press 'Yes' to reset the game.
6. Pressing no halts the game, you will have to close the window and restart.
7. If the game seems a little slow, open the file `junctionJam/models/cross/gui-settins.cfg` and decrease the delay to 1
   if it is too slow then you may need a faster computer.

## Problems
If you have issues installing the software please feel free to contact me. My details are on my 
[Github profile](https://github.com/cbrafter), please put the email subject as **Junction Jam: *subject***.
