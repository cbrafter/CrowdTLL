"""
@file    sumoConfigGen.py
@author  Craig Rafter
@date    29/01/2016

Code to generate a config file for a SUMO model.

"""


def sumoConfigGen(modelname='simpleT', configFile='./models/simpleT.sumocfg',
                  exportPath='../', AVratio=0, stepSize=0.01,
                  run=0, port=8813):
    configXML = open(configFile, 'w')
    print >> configXML, """<configuration>
    <input>
        <net-file value="{model}.net.xml"/>
        <route-files value="{model}.rou.xml"/>
        <gui-settings-file value="gui-settings.cfg"/>
        <game value="1"/>
        <start value="1"/>
        <!--additional-files value="{model}.det.xml"/-->
    </input>
    <output>
        <!--<summary-output value="{expPath}summary{AVR:03d}_{Nrun:03d}.xml"/>-->
        <!--tripinfo-output value="{expPath}tripinfo{AVR:03d}_{Nrun:03d}.xml"/-->
        <!--<vehroute-output value="{expPath}vehroute{AVR:03d}_{Nrun:03d}.xml"/-->
        <!--queue-output value="{expPath}queuedata{AVR:03d}_{Nrun:03d}.xml"/-->
    </output>
    <time>
        <begin value="0"/>
        <step-length value="{stepSz}"/>
    </time>
    <processing>
        <!--TURN OFF TELEPORTING-->
        <time-to-teleport value="-1"/>
    </processing>
    <report>
        <no-step-log value="true"/>
        <error-log value="logfile.txt"/>
    </report>
    <traci_server>
        <remote-port value="{SUMOport}"/>
    </traci_server>""".format(model=modelname, expPath=exportPath,
                              AVR=int(AVratio*100), stepSz=stepSize,
                              Nrun=run, SUMOport=port)
    print >> configXML, "</configuration>"
    configXML.close()
