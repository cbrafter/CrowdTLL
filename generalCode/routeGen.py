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

    elif ('twinT' in routeFile):
        print >> routes, """
    <route id="8to6" edges="8:2 2:0 0:1 1:5 5:6" />
    <route id="8to7" edges="8:2 2:0 0:1 1:3 3:7" />
    <route id="8to10" edges="8:2 2:0 0:9 9:10" />
    <route id="7to6" edges="7:3 3:1 1:5 5:6" />
    <route id="7to8" edges="7:3 3:1 1:0 0:2 2:8" />
    <route id="7to10" edges="7:3 3:1 1:0 0:9 9:10" />
    <route id="6to8" edges="6:5 5:1 1:0 0:2 2:8" />
    <route id="6to7" edges="6:5 5:1 1:3 3:7" />
    <route id="6to10" edges="6:5 5:1 1:0 0:9 9:10" />
    <route id="10to6" edges="10:9 9:0 0:1 1:5 5:6" />
    <route id="10to7" edges="10:9 9:0 0:1 1:3 3:7" />
    <route id="10to8" edges="10:9 9:0 0:2 2:8" />
    """
        prob = 0.04
        routeList = [
            ["8to6", prob],
            ["8to7", prob],
            ["8to10", prob],
            ["7to6", prob],
            ["7to8", prob],
            ["7to10", prob],
            ["6to8", prob],
            ["6to7", prob],
            ["6to10", prob],
            ["10to6", prob],
            ["10to7", prob],
            ["10to8", prob]
        ]

    elif ('corridor' in routeFile):
        print >> routes, """
    <route edges="6:4 4:0 0:10 10:11 " id="6:4TO10:11"/>
    <route edges="6:4 4:0 0:1 1:2 2:3 3:16 16:17 " id="6:4TO16:17"/>
    <route edges="6:4 4:0 0:1 1:2 2:3 3:5 5:7 " id="6:4TO5:7"/>
    <route edges="6:4 4:0 0:1 1:2 2:14 14:15 " id="6:4TO14:15"/>
    <route edges="6:4 4:0 0:8 8:9 " id="6:4TO8:9"/>
    <route edges="6:4 4:0 0:1 1:2 2:3 3:18 18:19 " id="6:4TO18:19"/>
    <route edges="6:4 4:0 0:1 1:12 12:13 " id="6:4TO12:13"/>
    <route edges="9:8 8:0 0:4 4:6 " id="9:8TO4:6"/>
    <route edges="9:8 8:0 0:1 1:2 2:3 3:16 16:17 " id="9:8TO16:17"/>
    <route edges="9:8 8:0 0:1 1:2 2:3 3:5 5:7 " id="9:8TO5:7"/>
    <route edges="9:8 8:0 0:1 1:2 2:14 14:15 " id="9:8TO14:15"/>
    <route edges="9:8 8:0 0:10 10:11 " id="9:8TO10:11"/>
    <route edges="9:8 8:0 0:1 1:2 2:3 3:18 18:19 " id="9:8TO18:19"/>
    <route edges="9:8 8:0 0:1 1:12 12:13 " id="9:8TO12:13"/>
    <route edges="11:10 10:0 0:4 4:6 " id="11:10TO4:6"/>
    <route edges="11:10 10:0 0:1 1:2 2:3 3:16 16:17 " id="11:10TO16:17"/>
    <route edges="11:10 10:0 0:1 1:2 2:3 3:5 5:7 " id="11:10TO5:7"/>
    <route edges="11:10 10:0 0:1 1:2 2:14 14:15 " id="11:10TO14:15"/>
    <route edges="11:10 10:0 0:8 8:9 " id="11:10TO8:9"/>
    <route edges="11:10 10:0 0:1 1:2 2:3 3:18 18:19 " id="11:10TO18:19"/>
    <route edges="11:10 10:0 0:1 1:12 12:13 " id="11:10TO12:13"/>
    <route edges="13:12 12:1 1:0 0:10 10:11 " id="13:12TO10:11"/>
    <route edges="13:12 12:1 1:2 2:14 14:15 " id="13:12TO14:15"/>
    <route edges="13:12 12:1 1:0 0:8 8:9 " id="13:12TO8:9"/>
    <route edges="13:12 12:1 1:2 2:3 3:16 16:17 " id="13:12TO16:17"/>
    <route edges="13:12 12:1 1:0 0:4 4:6 " id="13:12TO4:6"/>
    <route edges="13:12 12:1 1:2 2:3 3:5 5:7 " id="13:12TO5:7"/>
    <route edges="13:12 12:1 1:2 2:3 3:18 18:19 " id="13:12TO18:19"/>
    <route edges="15:14 14:2 2:1 1:12 12:13 " id="15:14TO12:13"/>
    <route edges="15:14 14:2 2:3 3:18 18:19 " id="15:14TO18:19"/>
    <route edges="15:14 14:2 2:3 3:16 16:17 " id="15:14TO16:17"/>
    <route edges="15:14 14:2 2:3 3:5 5:7 " id="15:14TO5:7"/>
    <route edges="15:14 14:2 2:1 1:0 0:8 8:9 " id="15:14TO8:9"/>
    <route edges="15:14 14:2 2:1 1:0 0:10 10:11 " id="15:14TO10:11"/>
    <route edges="15:14 14:2 2:1 1:0 0:4 4:6 " id="15:14TO4:6"/>
    <route edges="17:16 16:3 3:2 2:1 1:0 0:8 8:9 " id="17:16TO8:9"/>
    <route edges="17:16 16:3 3:5 5:7 " id="17:16TO5:7"/>
    <route edges="17:16 16:3 3:2 2:1 1:0 0:10 10:11 " id="17:16TO10:11"/>
    <route edges="17:16 16:3 3:2 2:1 1:0 0:4 4:6 " id="17:16TO4:6"/>
    <route edges="17:16 16:3 3:18 18:19 " id="17:16TO18:19"/>
    <route edges="17:16 16:3 3:2 2:1 1:12 12:13 " id="17:16TO12:13"/>
    <route edges="17:16 16:3 3:2 2:14 14:15 " id="17:16TO14:15"/>
    <route edges="19:18 18:3 3:2 2:1 1:0 0:8 8:9 " id="19:18TO8:9"/>
    <route edges="19:18 18:3 3:5 5:7 " id="19:18TO5:7"/>
    <route edges="19:18 18:3 3:2 2:1 1:0 0:10 10:11 " id="19:18TO10:11"/>
    <route edges="19:18 18:3 3:2 2:1 1:0 0:4 4:6 " id="19:18TO4:6"/>
    <route edges="19:18 18:3 3:16 16:17 " id="19:18TO16:17"/>
    <route edges="19:18 18:3 3:2 2:1 1:12 12:13 " id="19:18TO12:13"/>
    <route edges="19:18 18:3 3:2 2:14 14:15 " id="19:18TO14:15"/>
    <route edges="7:5 5:3 3:18 18:19 " id="7:5TO18:19"/>
    <route edges="7:5 5:3 3:2 2:1 1:0 0:8 8:9 " id="7:5TO8:9"/>
    <route edges="7:5 5:3 3:2 2:1 1:0 0:4 4:6 " id="7:5TO4:6"/>
    <route edges="7:5 5:3 3:2 2:1 1:12 12:13 " id="7:5TO12:13"/>
    <route edges="7:5 5:3 3:16 16:17 " id="7:5TO16:17"/>
    <route edges="7:5 5:3 3:2 2:1 1:0 0:10 10:11 " id="7:5TO10:11"/>
    <route edges="7:5 5:3 3:2 2:14 14:15 " id="7:5TO14:15"/>
    """

        prob = 0.015
        routeList = [
            ["6:4TO10:11", prob],
            ["6:4TO16:17", prob],
            ["6:4TO5:7", prob],
            ["6:4TO14:15", prob],
            ["6:4TO8:9", prob],
            ["6:4TO18:19", prob],
            ["6:4TO12:13", prob],
            ["9:8TO4:6", prob/3],
            ["9:8TO16:17", prob/3],
            ["9:8TO5:7", prob/3],
            ["9:8TO14:15", prob/3],
            ["9:8TO10:11", prob/3],
            ["9:8TO18:19", prob/3],
            ["9:8TO12:13", prob/3],
            ["11:10TO4:6", prob/3],
            ["11:10TO16:17", prob/3],
            ["11:10TO5:7", prob/3],
            ["11:10TO14:15", prob/3],
            ["11:10TO8:9", prob/3],
            ["11:10TO18:19", prob/3],
            ["11:10TO12:13", prob/3],
            ["13:12TO10:11", prob/3],
            ["13:12TO14:15", prob/3],
            ["13:12TO8:9", prob/3],
            ["13:12TO16:17", prob/3],
            ["13:12TO4:6", prob/3],
            ["13:12TO5:7", prob/3],
            ["13:12TO18:19", prob/3],
            ["15:14TO12:13", prob/3],
            ["15:14TO18:19", prob/3],
            ["15:14TO16:17", prob/3],
            ["15:14TO5:7", prob/3],
            ["15:14TO8:9", prob/3],
            ["15:14TO10:11", prob/3],
            ["15:14TO4:6", prob/3],
            ["17:16TO8:9", prob/3],
            ["17:16TO5:7", prob/3],
            ["17:16TO10:11", prob/3],
            ["17:16TO4:6", prob/3],
            ["17:16TO18:19", prob/3],
            ["17:16TO12:13", prob/3],
            ["17:16TO14:15", prob/3],
            ["19:18TO8:9", prob/3],
            ["19:18TO5:7", prob/3],
            ["19:18TO10:11", prob/3],
            ["19:18TO4:6", prob/3],
            ["19:18TO16:17", prob/3],
            ["19:18TO12:13", prob/3],
            ["19:18TO14:15", prob/3],
            ["7:5TO18:19", prob],
            ["7:5TO8:9", prob],
            ["7:5TO4:6", prob],
            ["7:5TO12:13", prob],
            ["7:5TO16:17", prob],
            ["7:5TO10:11", prob],
            ["7:5TO14:15", prob]
        ]

    elif ('manhattan' in routeFile):
        print >> routes, """
    <route edges="a1:b1 b1:c1 c1:c2 c2:b2 b2:b1 b1:a1" id="a1:b1TOb1:a1"/>
    <route edges="a1:b1 b1:b2 b2:a2" id="a1:b1TOb2:a2"/>
    <route edges="a1:b1 b1:b2 b2:b3 b3:a3" id="a1:b1TOb3:a3"/>
    <route edges="a1:b1 b1:b0" id="a1:b1TOb1:b0"/>
    <route edges="a1:b1 b1:c1 c1:c0" id="a1:b1TOc1:c0"/>
    <route edges="a1:b1 b1:c1 c1:d1 d1:d0" id="a1:b1TOd1:d0"/>
    <route edges="a1:b1 b1:b2 b2:b3 b3:b4" id="a1:b1TOb3:b4"/>
    <route edges="a1:b1 b1:b2 b2:b3 b3:c3 c3:c4" id="a1:b1TOc3:c4"/>
    <route edges="a1:b1 b1:b2 b2:b3 b3:c3 c3:d3 d3:d4" id="a1:b1TOd3:d4"/>
    <route edges="a1:b1 b1:c1 c1:d1 d1:e1" id="a1:b1TOd1:e1"/>
    <route edges="a1:b1 b1:b2 b2:c2 c2:d2 d2:e2" id="a1:b1TOd2:e2"/>
    <route edges="a1:b1 b1:b2 b2:b3 b3:c3 c3:d3 d3:e3" id="a1:b1TOd3:e3"/>
    <route edges="a2:b2 b2:b1 b1:a1" id="a2:b2TOb1:a1"/>
    <route edges="a2:b2 b2:c2 c2:c1 c1:b1 b1:b2 b2:a2" id="a2:b2TOb2:a2"/>
    <route edges="a2:b2 b2:b3 b3:a3" id="a2:b2TOb3:a3"/>
    <route edges="a2:b2 b2:b1 b1:b0" id="a2:b2TOb1:b0"/>
    <route edges="a2:b2 b2:b1 b1:c1 c1:c0" id="a2:b2TOc1:c0"/>
    <route edges="a2:b2 b2:b1 b1:c1 c1:d1 d1:d0" id="a2:b2TOd1:d0"/>
    <route edges="a2:b2 b2:b3 b3:b4" id="a2:b2TOb3:b4"/>
    <route edges="a2:b2 b2:b3 b3:c3 c3:c4" id="a2:b2TOc3:c4"/>
    <route edges="a2:b2 b2:b3 b3:c3 c3:d3 d3:d4" id="a2:b2TOd3:d4"/>
    <route edges="a2:b2 b2:b1 b1:c1 c1:d1 d1:e1" id="a2:b2TOd1:e1"/>
    <route edges="a2:b2 b2:c2 c2:d2 d2:e2" id="a2:b2TOd2:e2"/>
    <route edges="a2:b2 b2:b3 b3:c3 c3:d3 d3:e3" id="a2:b2TOd3:e3"/>
    <route edges="a3:b3 b3:b2 b2:b1 b1:a1" id="a3:b3TOb1:a1"/>
    <route edges="a3:b3 b3:b2 b2:a2" id="a3:b3TOb2:a2"/>
    <route edges="a3:b3 b3:c3 c3:c2 c2:b2 b2:b3 b3:a3" id="a3:b3TOb3:a3"/>
    <route edges="a3:b3 b3:b2 b2:b1 b1:b0" id="a3:b3TOb1:b0"/>
    <route edges="a3:b3 b3:b2 b2:b1 b1:c1 c1:c0" id="a3:b3TOc1:c0"/>
    <route edges="a3:b3 b3:b2 b2:b1 b1:c1 c1:d1 d1:d0" id="a3:b3TOd1:d0"/>
    <route edges="a3:b3 b3:b4" id="a3:b3TOb3:b4"/>
    <route edges="a3:b3 b3:c3 c3:c4" id="a3:b3TOc3:c4"/>
    <route edges="a3:b3 b3:c3 c3:d3 d3:d4" id="a3:b3TOd3:d4"/>
    <route edges="a3:b3 b3:b2 b2:b1 b1:c1 c1:d1 d1:e1" id="a3:b3TOd1:e1"/>
    <route edges="a3:b3 b3:b2 b2:c2 c2:d2 d2:e2" id="a3:b3TOd2:e2"/>
    <route edges="a3:b3 b3:c3 c3:d3 d3:e3" id="a3:b3TOd3:e3"/>
    <route edges="b0:b1 b1:a1" id="b0:b1TOb1:a1"/>
    <route edges="b0:b1 b1:b2 b2:a2" id="b0:b1TOb2:a2"/>
    <route edges="b0:b1 b1:b2 b2:b3 b3:a3" id="b0:b1TOb3:a3"/>
    <route edges="b0:b1 b1:c1 c1:c2 c2:b2 b2:b1 b1:b0" id="b0:b1TOb1:b0"/>
    <route edges="b0:b1 b1:c1 c1:c0" id="b0:b1TOc1:c0"/>
    <route edges="b0:b1 b1:c1 c1:d1 d1:d0" id="b0:b1TOd1:d0"/>
    <route edges="b0:b1 b1:b2 b2:b3 b3:b4" id="b0:b1TOb3:b4"/>
    <route edges="b0:b1 b1:b2 b2:b3 b3:c3 c3:c4" id="b0:b1TOc3:c4"/>
    <route edges="b0:b1 b1:b2 b2:b3 b3:c3 c3:d3 d3:d4" id="b0:b1TOd3:d4"/>
    <route edges="b0:b1 b1:c1 c1:d1 d1:e1" id="b0:b1TOd1:e1"/>
    <route edges="b0:b1 b1:b2 b2:c2 c2:d2 d2:e2" id="b0:b1TOd2:e2"/>
    <route edges="b0:b1 b1:b2 b2:b3 b3:c3 c3:d3 d3:e3" id="b0:b1TOd3:e3"/>
    <route edges="c0:c1 c1:b1 b1:a1" id="c0:c1TOb1:a1"/>
    <route edges="c0:c1 c1:b1 b1:b2 b2:a2" id="c0:c1TOb2:a2"/>
    <route edges="c0:c1 c1:b1 b1:b2 b2:b3 b3:a3" id="c0:c1TOb3:a3"/>
    <route edges="c0:c1 c1:b1 b1:b0" id="c0:c1TOb1:b0"/>
    <route edges="c0:c1 c1:c2 c2:b2 b2:b1 b1:c1 c1:c0" id="c0:c1TOc1:c0"/>
    <route edges="c0:c1 c1:d1 d1:d0" id="c0:c1TOd1:d0"/>
    <route edges="c0:c1 c1:b1 b1:b2 b2:b3 b3:b4" id="c0:c1TOb3:b4"/>
    <route edges="c0:c1 c1:c2 c2:c3 c3:c4" id="c0:c1TOc3:c4"/>
    <route edges="c0:c1 c1:c2 c2:c3 c3:d3 d3:d4" id="c0:c1TOd3:d4"/>
    <route edges="c0:c1 c1:d1 d1:e1" id="c0:c1TOd1:e1"/>
    <route edges="c0:c1 c1:c2 c2:d2 d2:e2" id="c0:c1TOd2:e2"/>
    <route edges="c0:c1 c1:c2 c2:c3 c3:d3 d3:e3" id="c0:c1TOd3:e3"/>
    <route edges="d0:d1 d1:c1 c1:b1 b1:a1" id="d0:d1TOb1:a1"/>
    <route edges="d0:d1 d1:c1 c1:b1 b1:b2 b2:a2" id="d0:d1TOb2:a2"/>
    <route edges="d0:d1 d1:c1 c1:b1 b1:b2 b2:b3 b3:a3" id="d0:d1TOb3:a3"/>
    <route edges="d0:d1 d1:c1 c1:b1 b1:b0" id="d0:d1TOb1:b0"/>
    <route edges="d0:d1 d1:c1 c1:c0" id="d0:d1TOc1:c0"/>
    <route edges="d0:d1 d1:d2 d2:c2 c2:c1 c1:d1 d1:d0" id="d0:d1TOd1:d0"/>
    <route edges="d0:d1 d1:c1 c1:b1 b1:b2 b2:b3 b3:b4" id="d0:d1TOb3:b4"/>
    <route edges="d0:d1 d1:c1 c1:c2 c2:c3 c3:c4" id="d0:d1TOc3:c4"/>
    <route edges="d0:d1 d1:d2 d2:d3 d3:d4" id="d0:d1TOd3:d4"/>
    <route edges="d0:d1 d1:e1" id="d0:d1TOd1:e1"/>
    <route edges="d0:d1 d1:d2 d2:e2" id="d0:d1TOd2:e2"/>
    <route edges="d0:d1 d1:d2 d2:d3 d3:e3" id="d0:d1TOd3:e3"/>
    <route edges="b4:b3 b3:b2 b2:b1 b1:a1" id="b4:b3TOb1:a1"/>
    <route edges="b4:b3 b3:b2 b2:a2" id="b4:b3TOb2:a2"/>
    <route edges="b4:b3 b3:a3" id="b4:b3TOb3:a3"/>
    <route edges="b4:b3 b3:b2 b2:b1 b1:b0" id="b4:b3TOb1:b0"/>
    <route edges="b4:b3 b3:b2 b2:b1 b1:c1 c1:c0" id="b4:b3TOc1:c0"/>
    <route edges="b4:b3 b3:b2 b2:b1 b1:c1 c1:d1 d1:d0" id="b4:b3TOd1:d0"/>
    <route edges="b4:b3 b3:c3 c3:c2 c2:b2 b2:b3 b3:b4" id="b4:b3TOb3:b4"/>
    <route edges="b4:b3 b3:c3 c3:c4" id="b4:b3TOc3:c4"/>
    <route edges="b4:b3 b3:c3 c3:d3 d3:d4" id="b4:b3TOd3:d4"/>
    <route edges="b4:b3 b3:b2 b2:b1 b1:c1 c1:d1 d1:e1" id="b4:b3TOd1:e1"/>
    <route edges="b4:b3 b3:b2 b2:c2 c2:d2 d2:e2" id="b4:b3TOd2:e2"/>
    <route edges="b4:b3 b3:c3 c3:d3 d3:e3" id="b4:b3TOd3:e3"/>
    <route edges="c4:c3 c3:b3 b3:b2 b2:b1 b1:a1" id="c4:c3TOb1:a1"/>
    <route edges="c4:c3 c3:b3 b3:b2 b2:a2" id="c4:c3TOb2:a2"/>
    <route edges="c4:c3 c3:b3 b3:a3" id="c4:c3TOb3:a3"/>
    <route edges="c4:c3 c3:b3 b3:b2 b2:b1 b1:b0" id="c4:c3TOb1:b0"/>
    <route edges="c4:c3 c3:c2 c2:c1 c1:c0" id="c4:c3TOc1:c0"/>
    <route edges="c4:c3 c3:c2 c2:c1 c1:d1 d1:d0" id="c4:c3TOd1:d0"/>
    <route edges="c4:c3 c3:b3 b3:b4" id="c4:c3TOb3:b4"/>
    <route edges="c4:c3 c3:c2 c2:b2 b2:b3 b3:c3 c3:c4" id="c4:c3TOc3:c4"/>
    <route edges="c4:c3 c3:d3 d3:d4" id="c4:c3TOd3:d4"/>
    <route edges="c4:c3 c3:c2 c2:c1 c1:d1 d1:e1" id="c4:c3TOd1:e1"/>
    <route edges="c4:c3 c3:c2 c2:d2 d2:e2" id="c4:c3TOd2:e2"/>
    <route edges="c4:c3 c3:d3 d3:e3" id="c4:c3TOd3:e3"/>
    <route edges="d4:d3 d3:c3 c3:b3 b3:b2 b2:b1 b1:a1" id="d4:d3TOb1:a1"/>
    <route edges="d4:d3 d3:c3 c3:b3 b3:b2 b2:a2" id="d4:d3TOb2:a2"/>
    <route edges="d4:d3 d3:c3 c3:b3 b3:a3" id="d4:d3TOb3:a3"/>
    <route edges="d4:d3 d3:c3 c3:b3 b3:b2 b2:b1 b1:b0" id="d4:d3TOb1:b0"/>
    <route edges="d4:d3 d3:c3 c3:c2 c2:c1 c1:c0" id="d4:d3TOc1:c0"/>
    <route edges="d4:d3 d3:d2 d2:d1 d1:d0" id="d4:d3TOd1:d0"/>
    <route edges="d4:d3 d3:c3 c3:b3 b3:b4" id="d4:d3TOb3:b4"/>
    <route edges="d4:d3 d3:c3 c3:c4" id="d4:d3TOc3:c4"/>
    <route edges="d4:d3 d3:d2 d2:c2 c2:c3 c3:d3 d3:d4" id="d4:d3TOd3:d4"/>
    <route edges="d4:d3 d3:d2 d2:d1 d1:e1" id="d4:d3TOd1:e1"/>
    <route edges="d4:d3 d3:d2 d2:e2" id="d4:d3TOd2:e2"/>
    <route edges="d4:d3 d3:e3" id="d4:d3TOd3:e3"/>
    <route edges="e1:d1 d1:c1 c1:b1 b1:a1" id="e1:d1TOb1:a1"/>
    <route edges="e1:d1 d1:c1 c1:b1 b1:b2 b2:a2" id="e1:d1TOb2:a2"/>
    <route edges="e1:d1 d1:c1 c1:b1 b1:b2 b2:b3 b3:a3" id="e1:d1TOb3:a3"/>
    <route edges="e1:d1 d1:c1 c1:b1 b1:b0" id="e1:d1TOb1:b0"/>
    <route edges="e1:d1 d1:c1 c1:c0" id="e1:d1TOc1:c0"/>
    <route edges="e1:d1 d1:d0" id="e1:d1TOd1:d0"/>
    <route edges="e1:d1 d1:c1 c1:b1 b1:b2 b2:b3 b3:b4" id="e1:d1TOb3:b4"/>
    <route edges="e1:d1 d1:c1 c1:c2 c2:c3 c3:c4" id="e1:d1TOc3:c4"/>
    <route edges="e1:d1 d1:d2 d2:d3 d3:d4" id="e1:d1TOd3:d4"/>
    <route edges="e1:d1 d1:d2 d2:c2 c2:c1 c1:d1 d1:e1" id="e1:d1TOd1:e1"/>
    <route edges="e1:d1 d1:d2 d2:e2" id="e1:d1TOd2:e2"/>
    <route edges="e1:d1 d1:d2 d2:d3 d3:e3" id="e1:d1TOd3:e3"/>
    <route edges="e2:d2 d2:c2 c2:b2 b2:b1 b1:a1" id="e2:d2TOb1:a1"/>
    <route edges="e2:d2 d2:c2 c2:b2 b2:a2" id="e2:d2TOb2:a2"/>
    <route edges="e2:d2 d2:c2 c2:b2 b2:b3 b3:a3" id="e2:d2TOb3:a3"/>
    <route edges="e2:d2 d2:c2 c2:b2 b2:b1 b1:b0" id="e2:d2TOb1:b0"/>
    <route edges="e2:d2 d2:c2 c2:c1 c1:c0" id="e2:d2TOc1:c0"/>
    <route edges="e2:d2 d2:d1 d1:d0" id="e2:d2TOd1:d0"/>
    <route edges="e2:d2 d2:c2 c2:b2 b2:b3 b3:b4" id="e2:d2TOb3:b4"/>
    <route edges="e2:d2 d2:c2 c2:c3 c3:c4" id="e2:d2TOc3:c4"/>
    <route edges="e2:d2 d2:d3 d3:d4" id="e2:d2TOd3:d4"/>
    <route edges="e2:d2 d2:d1 d1:e1" id="e2:d2TOd1:e1"/>
    <route edges="e2:d2 d2:d1 d1:c1 c1:c2 c2:d2 d2:e2" id="e2:d2TOd2:e2"/>
    <route edges="e2:d2 d2:d3 d3:e3" id="e2:d2TOd3:e3"/>
    <route edges="e3:d3 d3:c3 c3:b3 b3:b2 b2:b1 b1:a1" id="e3:d3TOb1:a1"/>
    <route edges="e3:d3 d3:c3 c3:b3 b3:b2 b2:a2" id="e3:d3TOb2:a2"/>
    <route edges="e3:d3 d3:c3 c3:b3 b3:a3" id="e3:d3TOb3:a3"/>
    <route edges="e3:d3 d3:c3 c3:b3 b3:b2 b2:b1 b1:b0" id="e3:d3TOb1:b0"/>
    <route edges="e3:d3 d3:c3 c3:c2 c2:c1 c1:c0" id="e3:d3TOc1:c0"/>
    <route edges="e3:d3 d3:d2 d2:d1 d1:d0" id="e3:d3TOd1:d0"/>
    <route edges="e3:d3 d3:c3 c3:b3 b3:b4" id="e3:d3TOb3:b4"/>
    <route edges="e3:d3 d3:c3 c3:c4" id="e3:d3TOc3:c4"/>
    <route edges="e3:d3 d3:d4" id="e3:d3TOd3:d4"/>
    <route edges="e3:d3 d3:d2 d2:d1 d1:e1" id="e3:d3TOd1:e1"/>
    <route edges="e3:d3 d3:d2 d2:e2" id="e3:d3TOd2:e2"/>
    <route edges="e3:d3 d3:d2 d2:c2 c2:c3 c3:d3 d3:e3" id="e3:d3TOd3:e3"/>
    """
    # Probabilities of car on trajectory
        prob = 0.003
        routeList = [
            ["a1:b1TOb1:a1", prob],
            ["a1:b1TOb2:a2", prob],
            ["a1:b1TOb3:a3", prob],
            ["a1:b1TOb1:b0", prob],
            ["a1:b1TOc1:c0", prob],
            ["a1:b1TOd1:d0", prob],
            ["a1:b1TOb3:b4", prob],
            ["a1:b1TOc3:c4", prob],
            ["a1:b1TOd3:d4", prob],
            ["a1:b1TOd1:e1", prob],
            ["a1:b1TOd2:e2", prob],
            ["a1:b1TOd3:e3", prob],
            ["a2:b2TOb1:a1", prob],
            ["a2:b2TOb2:a2", prob],
            ["a2:b2TOb3:a3", prob],
            ["a2:b2TOb1:b0", prob],
            ["a2:b2TOc1:c0", prob],
            ["a2:b2TOd1:d0", prob],
            ["a2:b2TOb3:b4", prob],
            ["a2:b2TOc3:c4", prob],
            ["a2:b2TOd3:d4", prob],
            ["a2:b2TOd1:e1", prob],
            ["a2:b2TOd2:e2", prob],
            ["a2:b2TOd3:e3", prob],
            ["a3:b3TOb1:a1", prob],
            ["a3:b3TOb2:a2", prob],
            ["a3:b3TOb3:a3", prob],
            ["a3:b3TOb1:b0", prob],
            ["a3:b3TOc1:c0", prob],
            ["a3:b3TOd1:d0", prob],
            ["a3:b3TOb3:b4", prob],
            ["a3:b3TOc3:c4", prob],
            ["a3:b3TOd3:d4", prob],
            ["a3:b3TOd1:e1", prob],
            ["a3:b3TOd2:e2", prob],
            ["a3:b3TOd3:e3", prob],
            ["b0:b1TOb1:a1", prob],
            ["b0:b1TOb2:a2", prob],
            ["b0:b1TOb3:a3", prob],
            ["b0:b1TOb1:b0", prob],
            ["b0:b1TOc1:c0", prob],
            ["b0:b1TOd1:d0", prob],
            ["b0:b1TOb3:b4", prob],
            ["b0:b1TOc3:c4", prob],
            ["b0:b1TOd3:d4", prob],
            ["b0:b1TOd1:e1", prob],
            ["b0:b1TOd2:e2", prob],
            ["b0:b1TOd3:e3", prob],
            ["c0:c1TOb1:a1", prob],
            ["c0:c1TOb2:a2", prob],
            ["c0:c1TOb3:a3", prob],
            ["c0:c1TOb1:b0", prob],
            ["c0:c1TOc1:c0", prob],
            ["c0:c1TOd1:d0", prob],
            ["c0:c1TOb3:b4", prob],
            ["c0:c1TOc3:c4", prob],
            ["c0:c1TOd3:d4", prob],
            ["c0:c1TOd1:e1", prob],
            ["c0:c1TOd2:e2", prob],
            ["c0:c1TOd3:e3", prob],
            ["d0:d1TOb1:a1", prob],
            ["d0:d1TOb2:a2", prob],
            ["d0:d1TOb3:a3", prob],
            ["d0:d1TOb1:b0", prob],
            ["d0:d1TOc1:c0", prob],
            ["d0:d1TOd1:d0", prob],
            ["d0:d1TOb3:b4", prob],
            ["d0:d1TOc3:c4", prob],
            ["d0:d1TOd3:d4", prob],
            ["d0:d1TOd1:e1", prob],
            ["d0:d1TOd2:e2", prob],
            ["d0:d1TOd3:e3", prob],
            ["b4:b3TOb1:a1", prob],
            ["b4:b3TOb2:a2", prob],
            ["b4:b3TOb3:a3", prob],
            ["b4:b3TOb1:b0", prob],
            ["b4:b3TOc1:c0", prob],
            ["b4:b3TOd1:d0", prob],
            ["b4:b3TOb3:b4", prob],
            ["b4:b3TOc3:c4", prob],
            ["b4:b3TOd3:d4", prob],
            ["b4:b3TOd1:e1", prob],
            ["b4:b3TOd2:e2", prob],
            ["b4:b3TOd3:e3", prob],
            ["c4:c3TOb1:a1", prob],
            ["c4:c3TOb2:a2", prob],
            ["c4:c3TOb3:a3", prob],
            ["c4:c3TOb1:b0", prob],
            ["c4:c3TOc1:c0", prob],
            ["c4:c3TOd1:d0", prob],
            ["c4:c3TOb3:b4", prob],
            ["c4:c3TOc3:c4", prob],
            ["c4:c3TOd3:d4", prob],
            ["c4:c3TOd1:e1", prob],
            ["c4:c3TOd2:e2", prob],
            ["c4:c3TOd3:e3", prob],
            ["d4:d3TOb1:a1", prob],
            ["d4:d3TOb2:a2", prob],
            ["d4:d3TOb3:a3", prob],
            ["d4:d3TOb1:b0", prob],
            ["d4:d3TOc1:c0", prob],
            ["d4:d3TOd1:d0", prob],
            ["d4:d3TOb3:b4", prob],
            ["d4:d3TOc3:c4", prob],
            ["d4:d3TOd3:d4", prob],
            ["d4:d3TOd1:e1", prob],
            ["d4:d3TOd2:e2", prob],
            ["d4:d3TOd3:e3", prob],
            ["e1:d1TOb1:a1", prob],
            ["e1:d1TOb2:a2", prob],
            ["e1:d1TOb3:a3", prob],
            ["e1:d1TOb1:b0", prob],
            ["e1:d1TOc1:c0", prob],
            ["e1:d1TOd1:d0", prob],
            ["e1:d1TOb3:b4", prob],
            ["e1:d1TOc3:c4", prob],
            ["e1:d1TOd3:d4", prob],
            ["e1:d1TOd1:e1", prob],
            ["e1:d1TOd2:e2", prob],
            ["e1:d1TOd3:e3", prob],
            ["e2:d2TOb1:a1", prob],
            ["e2:d2TOb2:a2", prob],
            ["e2:d2TOb3:a3", prob],
            ["e2:d2TOb1:b0", prob],
            ["e2:d2TOc1:c0", prob],
            ["e2:d2TOd1:d0", prob],
            ["e2:d2TOb3:b4", prob],
            ["e2:d2TOc3:c4", prob],
            ["e2:d2TOd3:d4", prob],
            ["e2:d2TOd1:e1", prob],
            ["e2:d2TOd2:e2", prob],
            ["e2:d2TOd3:e3", prob],
            ["e3:d3TOb1:a1", prob],
            ["e3:d3TOb2:a2", prob],
            ["e3:d3TOb3:a3", prob],
            ["e3:d3TOb1:b0", prob],
            ["e3:d3TOc1:c0", prob],
            ["e3:d3TOd1:d0", prob],
            ["e3:d3TOb3:b4", prob],
            ["e3:d3TOc3:c4", prob],
            ["e3:d3TOd3:d4", prob],
            ["e3:d3TOd1:e1", prob],
            ["e3:d3TOd2:e2", prob],
            ["e3:d3TOd3:e3", prob]
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
