# CrowdTLL
Crowd sourced traffic light control for outreach events.

*Please acknowledge the author and other relevant contributors in any derivative works.*

*Copyright 2017: Craig B. Rafter*

*Distributed under GNU GPL v3.0*

## Description
A simple crossroads simulated using the [TraCI](http://sumo.dlr.de/wiki/TraCI) [Python](https://www.python.org/) API to the [SUMO](http://www.sumo.dlr.de/) microsimulator. The program maps the keyboard arrow keys to control the direction of the traffic flow using the [Pynput](https://pypi.python.org/pypi/pynput) Python library. The *sumoAPI* included is from the [Traffic Control Test Set](http://tctester.sourceforge.net/).

The background overlay was created using [GIMP](https://www.gimp.org/), art credits below. Given the intention of displaying this to a wide audience, the vehicles are colored in a color blind accessible color palette.

## Future work
- Log user data so that machine learning can be applied to good user scores.
- Create a leaderboard so that users at events can see how their results compare.
- Simulation reloads automatically.

## Screenshot
![alt text](./images/screenshot_CTLL.png "A screenschot of CrowdTLL in action.")

## Requirements
System built and tested on:
- Ubuntu 16.04.1 LTS
- SUMO 0.28.0
- Python 2.7
- Pynput 1.2

## Acknowledgements
###Pixel Art:
**Trees:**
- René Alejandro Hernández [HERE](https://design.tutsplus.com/tutorials/how-to-create-an-isometric-pixel-art-tree-in-adobe-photoshop--cms-23606)
- User "shimauma" [HERE](https://forum.unity3d.com/threads/pixel-art-how-to-keep-original-sprite-size-in-game.241281/)

**Buildings:**
- User "JSena" [PixelJoint](http://pixeljoint.com/pixelart/44722.htm)
- User "duyvi" [PixelJoint](http://pixeljoint.com/p/9540.htm)
- User "Matriax" [PixelJoint](http://pixeljoint.com/p/644.htm)

### Color blind accessible color palette
Wong, B. *"Points of view: Color blindness"*, Nature Methods, 8, 441, 2011, [doi:10.1038/nmeth.1618](http://www.nature.com/nmeth/journal/v8/n6/full/nmeth.1618.html) 
