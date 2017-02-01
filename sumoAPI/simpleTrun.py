import fixedTimeControl,sumoConnect, readJunctionData

connector = sumoConnect.sumoConnect("../SimpleT/simpleT.sumocfg",True)

connector.launchSumoAndConnect()

jd = readJunctionData.readJunctionData("../SimpleT/simpleT.jcn.xml")
junctionsList = jd.getJunctionData()

controllerList=[]

for junction in junctionsList:
    controllerList.append(fixedTimeControl.fixedTimeControl(junction))

step = 0

while step == 0 or connector.traci.simulation.getMinExpectedNumber() > 0:
    connector.runSimulationForSeconds(1)
    for controller in controllerList:
        controller.process()



