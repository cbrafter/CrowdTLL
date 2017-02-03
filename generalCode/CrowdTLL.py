# -*- coding: utf-8 -*-
"""
@file    test.py
@author  Craig Rafter
@date    01/02/17

Code to run the "simpleT" SUMO model.
cd .
"""
import sys
import os
sys.path.insert(0, '../sumoAPI')
import sumoConnect
import readJunctionData
import traci
from keyControl import keyControl
from routeGen import routeGen
from sumoConfigGen import sumoConfigGen
from pynput import keyboard

global keyCapture
keyCapture = None


def on_release(key):
    global keyCapture
    keyCapture = '{0}'.format(key)

# Define road model directory
modelname = 'cross'
model = './models/{}/'.format(modelname)
# Generate new routes
N = 100  # Last time to insert vehicle at
stepSize = 0.1
vehNr, lastVeh = routeGen(N, routeFile=model + modelname + '.rou.xml')
print(vehNr, lastVeh)
print('Routes generated')

# Edit the the output filenames in sumoConfig
configFile = model + modelname + ".sumocfg"
exportPath = '../../results/'
# this is relative to script not cfg file
if not os.path.exists(model+exportPath):
    os.makedirs(model+exportPath)

simport = 8813  # TraCI connection port
# Configre Simulation parameters
sumoConfigGen(modelname, configFile, exportPath, stepSize, port=simport)

# Connect to model
connector = sumoConnect.sumoConnect(model + modelname + ".sumocfg",
                                    gui=True, port=simport)
connector.launchSumoAndConnect()
print('Model connected')

# Get junction data and configure the controller
jd = readJunctionData.readJunctionData(model + modelname + ".jcn.xml")
junctionsList = jd.getJunctionData()
TLcontroller = keyControl(junctionsList[0])
print('Junctions and controllers acquired')

# Step simulation while there are vehicles
keyLogger = keyboard.Listener(on_press=None, on_release=on_release)
keyLogger.start()
while traci.simulation.getMinExpectedNumber():
    # Step simulation and set controller state
    traci.simulationStep()
    
    # print(keyCapture)
    TLcontroller.process(keyCapture)

# Clean up
print("Disconnecting Keylogger")
keyLogger.stop()
print("Disconnecting from SUMO")
connector.disconnect()
print('Simulation Complete')
