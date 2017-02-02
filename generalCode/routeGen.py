#!/usr/bin/env python
"""
@file    routeGen.py
@author  Simon Box, Craig Rafter
@date    29/01/2016

Code to generate a routes file for the "simpleT" SUMO model.

"""
import random


def randCF(AVratio):
    ''' Assign random car following model based on AVratio
    '''
    return 'Human' if random.uniform(0, 1) >= AVratio else 'ITSCV'


def routeStr(vehNr, CFmodel, heading, Tdepart):
    ''' Generate XML route definition
    '''
    vID = 'vehicle id="%i" ' % (vehNr)
    vtype = 'type="type%s" ' % (CFmodel)
    route = 'route="%s" ' % (heading)
    depart = 'depart="%i" ' % (Tdepart)
    return '    <' + vID + vtype + route + depart + '/>'


def routeGen(N, AVratio=0, AVtau=0.1, routeFile='./simpleT.rou.xml'): 
    assert 0.0 <= AVratio <= 1.0, "Error: AVratio not between 0,1"
    assert '.rou.xml' == routeFile[-8:], "Error: Wrong route file extension"

    # Open routefile for writing
    routes = open(routeFile, "w")
    # Insert route file header
    print >> routes, """<routes>
    <vType id="typeHuman" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="25" guiShape="passenger" color="1,1,0">
    </vType>

    <vType id="typeITSCV" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="25" guiShape="passenger" color="1,0,0">
        <carFollowing-Krauss tau="{AVtau}"/>
    </vType>""".format(AVtau=AVtau)


    if ('plainRoad' in routeFile):
        print >> routes, """
    <route id="eastWest" edges="4:3 3:2 2:1 1:0" />
    <route id="westEast" edges="0:1 1:2 2:3 3:4" />
    """
        # Probabilities of car on trajectory
        routeList = [
            ['eastWest', 1.0/2.0], 
            ['westEast', 1.0/2.0]
        ]


    if ('simpleT' in routeFile):
        print >> routes, """
    <route id="eastSouth" edges="2:0 0:1 1:5 5:6" />
    <route id="eastWest" edges="2:0 0:1 1:3 3:7" />
    <route id="westSouth" edges="7:3 3:1 1:5 5:6" />
    <route id="westEast" edges="7:3 3:1 1:0 0:2" />
    <route id="southEast" edges="6:5 5:1 1:0 0:2" />
    <route id="southWest" edges="6:5 5:1 1:3 3:7" />
    """
        # Probabilities of car on trajectory
        routeList = [
            ['eastSouth', 1.0/30.0], 
            ['eastWest', 1.0/10.0], 
            ['westSouth', 1.0/30.0], 
            ['westEast', 1.0/10.0], 
            ['southEast', 1.0/50.0], 
            ['southWest', 1.0/50.0]
        ]

    if ('cross' in routeFile):
        print >> routes, """
    <route id="northEast"  edges="1:0 0:2" />
    <route id="northSouth" edges="1:0 0:3" />
    <route id="northWest"  edges="1:0 0:4" />
    <route id="eastNorth"  edges="2:0 0:1" />
    <route id="eastSouth"  edges="2:0 0:3" />
    <route id="eastWest"   edges="2:0 0:4" />
    <route id="southNorth" edges="3:0 0:1" />
    <route id="southEast"  edges="3:0 0:2" />
    <route id="southWest"  edges="3:0 0:4" />
    <route id="westNorth"  edges="4:0 0:1" />
    <route id="westEast"   edges="4:0 0:2" />
    <route id="westSouth"  edges="4:0 0:3" />
    """
        prob = 0.08
        routeList = [
            ["northEast", prob],
            ["northSouth", prob],
            ["northWest", prob],
            ["eastNorth", prob],
            ["eastSouth", prob],
            ["eastWest", prob],
            ["southNorth", prob],
            ["southEast", prob],
            ["southWest", prob],
            ["westNorth", prob],
            ["westEast", prob],
            ["westSouth", prob]
        ]

    lastVeh = 0
    vehNr = 0
    for i in range(N):
        for routeInfo in routeList:
            if random.uniform(0, 1) < routeInfo[1]:
                print >> routes, routeStr(vehNr, randCF(AVratio), routeInfo[0], i)
                vehNr += 1
                lastVeh = i

    print >> routes, "</routes>"
    routes.close()
    return vehNr, lastVeh
