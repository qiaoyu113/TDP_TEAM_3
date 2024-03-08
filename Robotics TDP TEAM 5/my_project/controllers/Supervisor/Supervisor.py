

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Basics.GameSupervisorCore import GameSupervisorCore
from Utils.Consts import (TIME_STEP, Motions)
from Scoreboard import Scoreboard

supervisor = GameSupervisorCore()
scoreboard = Scoreboard()

while supervisor.step(TIME_STEP) != -1:
    # The following code must be run to send the ball data to robots via emitter.
    # print("Robot RED_FW: ", supervisor.fetchRobotLocation("RED_FW"))
    scoreboard.updateScoreboard(supervisor)
    supervisor.transmitSupervisorInformation()
    #print("Supervisor: ", supervisor.fetchCurrentBallPosition())
    
