# -*- coding: utf-8 -*-
"""
@file    test.py
@author  Craig Rafter
@date    01/02/17

Code to run the "CrowdTLL" SUMO model.
"""
import sys
import os
import psutil
sys.path.insert(0, '../sumoAPI')
import sumoConnect
import readJunctionData
import traci
import updateResults
import messageBox as mbox
from time import strftime
from keyControl import keyControl
from routeGen import routeGen
from sumoConfigGen import sumoConfigGen
from pynput import keyboard

global keyCapture
keyCapture = None


def on_release(key):
    """Pynput thread trigger function that stores the value of the last released
    key press"""
    global keyCapture
    keyCapture = '{}'.format(key)

# Define road model directory
modelname = 'cross'
model = './models/{}/'.format(modelname)
# Generate new routes
N = 100  # Last time to insert vehicle at
stepSize = 0.1
#vehNr, lastVeh = routeGen(N, routeFile=model + modelname + '.rou.xml')
#print(vehNr, lastVeh)
#print('Routes generated')

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
while True:
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
    initial = mbox.mbox('Get ready to start!\nPlease enter your INITIALS:', entry=True)

    print traci.gui.setBoundary('View #0', -132.241238793806, 2.952380952380963,
        332.241238793806, 201.04761904761904)
    while traci.simulation.getMinExpectedNumber():
        # Step simulation and set controller state
        #print traci.gui.getBoundary('View #0')
        traci.simulationStep()
        
        # print(keyCapture)
        TLcontroller.process(keyCapture)

    # Log run data
    endTime = traci.simulation.getCurrentTime()*1e-3
    fname = './data/' + strftime('%Y_%m_%d_%H')
    print endTime
    #updateResults.updateResults(fname, initial, endTime)

    # Clean up
    print("Disconnecting Keylogger")
    keyLogger.stop()
    print("Disconnecting from SUMO")
    connector.disconnect()
    print('Simulation Complete')

    # Close the sumo-gui
    try:
        for process in psutil.process_iter():
            if process.name() == 'sumo-gui':
                process.terminate()
    except:
        pass
