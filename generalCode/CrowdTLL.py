# -*- coding: utf-8 -*-
"""
@file    CrowdTLL.py
@author  Craig Rafter
@date    01/02/17

Code to run the "CrowdTLL" SUMO game.
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
import twitAuth

global keyCapture
keyCapture = None


def on_release(key):
    """Pynput thread trigger function that stores the value of the last released
    key press"""
    global keyCapture
    keyCapture = '{}'.format(key)

# Set up display and logging options
online = 'online' in sys.argv  # tweet results
display = 'display' in sys.argv  # display results locally
if online:
    api = twitAuth.getAPI()

# Define road model directory
modelname = 'cross'
model = './models/{}/'.format(modelname)
# Generate new routes
N = 100  # Last time to insert vehicle at
stepSize = 0.1
# vehNr, lastVeh = routeGen(N, routeFile=model + modelname + '.rou.xml')
# print(vehNr, lastVeh)
# print('Routes generated')

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

    # Begin Gathering keypresses to control the traffic lights
    keyLogger = keyboard.Listener(on_press=None, on_release=on_release)
    keyLogger.start()

    # Get user initial 
    if online or display:
        initial = mbox.mbox('Get ready to start!\nPlease enter your INITIALS:',
                            entry=True)
    else:
        mbox.mbox('Get ready to start!')

    # Step simulation while there are vehicles
    while traci.simulation.getMinExpectedNumber():
        # Step simulation and set controller state
        traci.simulationStep()

        # Update TLL based on key pressed
        TLcontroller.process(keyCapture)

    # Log run data
    endTime = traci.simulation.getCurrentTime()*1e-3
    fname = './data/' + strftime('%Y_%m_%d_%H')

    # If online tweet results, if display log and generate results,
    # else do nothing
    if online:
        updateResults.tweetInfo(api, initial, endTime)
    elif display:
        # if the file for the current hour doesn't exist then open in
        # web broswer after creation
        if not os.path.exists(fname + '.html'):
            updateResults.updateResults(fname, initial, endTime)
            updateResults.openHTML_Browser(fname + '.html')
        else:
            updateResults.updateResults(fname, initial, endTime)
    else:
        pass

    # Clean up
    print("Disconnecting Keylogger")
    keyLogger.stop()
    print("Disconnecting from SUMO")
    connector.disconnect()
    print('Simulation Complete')

    # Close the sumo-gui as it doesn't handle itself
    # https://stackoverflow.com/questions/17856928/how-to-terminate-process-from-python-using-pid
    try:
        for process in psutil.process_iter():
            if process.name() == 'sumo-gui':
                process.terminate()
    except:
        pass
