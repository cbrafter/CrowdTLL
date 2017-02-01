"""
@file    simpleTwithTrafcod.py
@author  Simon Box and(?) Peter Knoppers
@date    12/02/2013

Control script for launching the simpleT SUMO model and then launching Trafcod and coordinating control.

"""
import sumoConnect, traci, trafcodLink

##STEP 1 - Launch SUMO ##############################################################

connector = sumoConnect.sumoConnect("../SimpleTtrafcodVersion/simpleT.sumocfg",True)
connector.launchSumoAndConnect()
######################################################################################

##STEP 2 - Launch Trafcod ############################################################
tcConnect = trafcodLink.trafcodLink('localhost',10000)##Listen for trafcod on port (arg2)

#tcConnect.launchTrafcod("trafcod.exe", "rules.tfc")#//TODO: This line has not yet been tested/debugged
tcConnect.handshakeTrafcod()

if tcConnect.connected:
    print "Connected to trafcod via %s port %s" % (tcConnect.clientAddress[0],tcConnect.clientAddress[1])
else:
    print "Failed to connect to Trafcod"
######################################################################################


##STEP 3 - Coordinate junction control################################################
junctionID = "1"##The ID for the junction when communicating with SUMO
detectorIDs = ["0","1","2","3","4","5","6","7","8","9"]##The IDs for the loops when communicating with SUMO
step = 0

while step == 0 or connector.traci.simulation.getMinExpectedNumber() > 0:
    
    ##STEP 3.1 - Advance SUMO one step################################################
    connector.runSimulationForOneStep()## Will advance the simulation by 0.1 seconds
    ##################################################################################
    
    ##STEP 3.2 - Collect Loop occupancy data #########################################
    
    ##Option 1 Use Python script #####################################################
    loopOccupancyValues = [] ## 0 = "not occupied during timestep"; 1 = "occupied during timestep"
    
    for detector in detectorIDs:
        occupied = traci.inductionloop.getLastStepVehicleNumber(detector)
        loopOccupancyValues.append(occupied)
        tcConnect.sendDetectorToTrafcod(detector, occupied)
    
    
    ##################################################################################
    
    ##Option 2 Let Trafcod query SUMO directly over tcp/ip############################
    #tcpPort = connector.Port
    
    #for detector in detectorIDs:
    #    pass##//TODO: Insert code triggering Trafcod to directly query detector data using
            ##tcpPort and detector following the protocol described here: http://sumo.sourceforge.net/doc/current/docs/userdoc/TraCI/Induction_Loop_Value_Retrieval.html
    
    ##################################################################################
    ##################################################################################
    
    ##STEP 3.3 - Return Signal control command to SUMO ###############################
    
    ##Option 1 Use Python script #####################################################
    tcConnect.askTrafcodToAdvance()#Ask TrafCod to calculate light states
    junctionLightData = tcConnect.recieveTrafcodLightStates()
    
    for junctionLight in junctionLightData:
        traci.trafficlights.setRedYellowGreenState(junctionLight[0], junctionLight[1])## Set the traffic lights in SUMO
    ##################################################################################
    
    ##Option 2 Let Trafcod set the lights in SUMO directly over tcp/ip################
    #tcpPort = connector.Port
    
    ##//TODO: Insert code triggering Trafcod to directly set traffic light state using
    ##a "control string" and the junction ID.
    ##################################################################################
    ##################################################################################
    
######################################################################################

##STEP 4 - Exit SUMO #################################################################
connector.disconnect()
######################################################################################

##STEP 5 - Exit Trafcod ##############################################################
tcConnect.closeTrafcod()
######################################################################################