"""
The Basic Supervisor class.
All Supervisor classes should be derived from this class.
"""

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from controller import Supervisor
import struct
from Utils.Consts import (TIME_STEP)
from Utils import Functions

class GameSupervisorCore(Supervisor):
  def __init__(self):
    super().__init__()

    self.emitter = self.getDevice("emitter")

    self.ball = self.getFromDef("SOCCERBALL")

    self.robots = {
      "RED_GK"    : self.getFromDef("RED_GK"),
      "RED_DEF_L" : self.getFromDef("RED_DEF_L"),
      "RED_DEF_R" : self.getFromDef("RED_DEF_R"),
      "RED_FW"    : self.getFromDef("RED_FW"),
      "BLUE_GK"   : self.getFromDef("BLUE_GK"),
      "BLUE_DEF"  : self.getFromDef("BLUE_DEF"),
      "BLUE_FW_L" : self.getFromDef("BLUE_FW_L"),
      "BLUE_FW_R" : self.getFromDef("BLUE_FW_R")
    }

    self.ballPriority = "R"

    self.previousBallLocation = [0, 0, 0.0798759]
  
  def fetchCurrentBallPosition(self) -> list:
    """Get the soccer ball coordinate on the field.

    Returns:
        list: x, y, z coordinates.
    """
    ballTranslation = self.ball.getField("translation")
    newBallLocation = ballTranslation.getSFVec3f()

    if abs(newBallLocation[0]) < 4.5 and abs(newBallLocation[1]) < 3:
      if (self.previousBallLocation[0] + 0.05 < newBallLocation[0] or self.previousBallLocation[0] - 0.05 > newBallLocation[0] or\
          self.previousBallLocation[1] + 0.05 < newBallLocation[1] or self.previousBallLocation[1] - 0.05 > newBallLocation[1]):
        self.ballPriority = "N"
        self.previousBallLocation = newBallLocation


    return newBallLocation
  
  def updateBallPositionOnField(self, ballPosition) -> None:
    """Set the soccer ball coordinate on the field.

    Args:
        list: x, y, z coordinates.
    """
    self.previousBallLocation = ballPosition
    ballTranslation = self.ball.getField("translation")
    ballTranslation.setSFVec3f(ballPosition)
    self.ball.resetPhysics()

  def fetchRobotLocation(self, robotName) -> list:
    """Get the robot coordinate on the field.

    Returns:
        list: x, y, z coordinates.
    """
    robotTranslation = self.robots[robotName].getField("translation")
    return robotTranslation.getSFVec3f()

  def calculateBallOwnership(self) -> str:
    """Calculate the ball owner team from the distances from the ball.

    Returns:
        str: Ball owner team first letter.
    """

    ballPosition = self.fetchCurrentBallPosition()
    ballOwnerRobotName = "RED_GK"
    minDistance = Functions.calculateDistance(ballPosition, self.fetchRobotLocation(ballOwnerRobotName))
    for i, key in enumerate(self.robots):
      tempDistance = Functions.calculateDistance(ballPosition, self.fetchRobotLocation(key))
      if tempDistance < minDistance:
        minDistance = tempDistance
        ballOwnerRobotName = key

    if len(ballOwnerRobotName) < 9:
      for i in range(len(ballOwnerRobotName), 9):
        ballOwnerRobotName = ballOwnerRobotName + '*'

    return ballOwnerRobotName

  def transmitSupervisorInformation(self) -> None:
    """Send Data (ballPosition, ballOwner, ballPriority, ...) to Robots. Channel is '0'."""
    
    ballPosition = self.fetchCurrentBallPosition()
    ballOwner = bytes(self.calculateBallOwnership(), 'utf-8')
    ballPriority = bytes(self.ballPriority, 'utf-8')

    redGk = self.fetchRobotLocation("RED_GK")
    redDefLeft = self.fetchRobotLocation("RED_DEF_L")
    redDefRight = self.fetchRobotLocation("RED_DEF_R")
    redFw = self.fetchRobotLocation("RED_FW")
    blueGk = self.fetchRobotLocation("BLUE_GK")
    blueDef = self.fetchRobotLocation("BLUE_DEF")
    blueFwLeft = self.fetchRobotLocation("BLUE_FW_L")
    blueFwRight = self.fetchRobotLocation("BLUE_FW_R")

    data = struct.pack('dd9ss24d', ballPosition[0], ballPosition[1], ballOwner, ballPriority, redGk[0], redGk[1], redGk[2], redDefLeft[0], redDefLeft[1], redDefLeft[2], redDefRight[0], redDefRight[1], redDefRight[2],\
                                  redFw[0], redFw[1], redFw[2], blueGk[0], blueGk[1], blueGk[2], blueDef[0], blueDef[1], blueDef[2], blueFwLeft[0], blueFwLeft[1], blueFwLeft[2], blueFwRight[0], blueFwRight[1], blueFwRight[2])
    self.emitter.send(data)

  def updateBallControlPriority(self, priority):
    self.ballPriority = priority

  def initializeSimulationState(self):
    self.previousBallLocation = [0, 0, 0.0798759]
    self.simulationReset()
    for robot in self.robots.values():
      robot.resetPhysics()
  
  def pauseSimulationExecution(self):
    self.simulationSetMode(self.SIMULATION_MODE_PAUSE)
