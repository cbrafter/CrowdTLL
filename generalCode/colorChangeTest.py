# -*- coding: utf-8 -*-
"""
@file    simpleTmixedVehicle.py
@author  Simon Box, Craig Rafter
@date    29/01/2016

Code to run the "simpleT" SUMO model.

"""
import sys, os
sys.path.insert(0, '../sumoAPI')
import fixedTimeControl
import sumoConnect
import readJunctionData
import traci
from routeGen import routeGen
from sumoConfigGen import sumoConfigGen
import numpy as np

# Define road model directory
modelname = 'simpleT'
model = './models/{}/'.format(modelname)
# Generate new routes
N = 5000  # Last time to insert vehicle at
stepSize = 0.1
AVratio = 1
AVtau = 1.0
vehNr, lastVeh = routeGen(N, AVratio, AVtau, routeFile=model + modelname + '.rou.xml')
print(vehNr, lastVeh)
print('Routes generated')

# Edit the the output filenames in sumoConfig
configFile = model + modelname + ".sumocfg"
exportPath = '../../simple/'
if not os.path.exists(model+exportPath): # this is relative to script not cfg file
    os.makedirs(model+exportPath)

simport = 8000
sumoConfigGen(modelname, configFile, exportPath, stepSize, port=simport)

# Connect to model
connector = sumoConnect.sumoConnect(model + modelname + ".sumocfg", gui=True, port=simport)
connector.launchSumoAndConnect()
print('Model connected')

# Get junction data
jd = readJunctionData.readJunctionData(model + modelname + ".jcn.xml")
junctionsList = jd.getJunctionData()

# Add controller models to junctions
controllerList = []
for junction in junctionsList:
    controllerList.append(fixedTimeControl.fixedTimeControl(junction))

print('Junctions and controllers acquired')

# Step simulation while there are vehicles
vehIDs = []
juncIDs = traci.trafficlights.getIDList()
juncPos = [traci.junction.getPosition(juncID) for juncID in juncIDs]

while traci.simulation.getMinExpectedNumber():
    traci.simulationStep()
    for controller in controllerList:
        controller.process()
    
    # if a vehicle within 50m of junction change col to red
    for vehID in traci.vehicle.getIDList():
        vehPos = traci.vehicle.getPosition(vehID)

        delta = 1e6
        for junc in juncPos:
            delta = min(delta, np.linalg.norm(np.diff([vehPos, junc], axis=0)))

        if delta < 50:
            traci.vehicle.setColor(vehID, (255,0,0,0))
            traci.vehicle.setSpeed(vehID, 5)
        else:
            traci.vehicle.setColor(vehID, (255,255,0,0))
            traci.vehicle.setSpeed(vehID, -1)


connector.disconnect()
print('DONE')
