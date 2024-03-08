"""
This is the scoreboard and timer class.
"""

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import time
from Utils.Consts import (TIME_STEP, BALL_POSITIONS)

class Scoreboard:
  def __init__(self):
    self.initialTimeMinutes = 10
    self.initialTimeSeconds = 0
    self.timeStepNormalizer = 0

    self.redTeamScore = 0
    self.blueTeamScore = 0

    self.latestGoalTime = 0

  def resetScoreboard(self):
    self.__init__()

  def updateScoreboard(self, supervisor):
    self.updateTimer(supervisor)
    self.checkBall(supervisor)

  def updateTimer(self, supervisor):
    self.timeRemainMinutes = self.initialTimeMinutes
    self.timeRemain_s = self.initialTimeSeconds    

    self.timeStepNormalizer += 1
    if self.timeStepNormalizer == 600/TIME_STEP:
      if self.timeRemain_s == 0:
        self.timeRemainMinutes -= 1
        self.initialTimeMinutes = self.timeRemainMinutes
        self.initialTimeSeconds = 60    
        self.timeRemain_s = self.initialTimeSeconds
          
      self.timeRemain_s -= 1
      if self.timeRemainMinutes == 0 and self.timeRemain_s == 0:
        print("TIME OUT!")
        print(f"RESULT: RED {self.redTeamScore} - {self.blueTeamScore} BLUE")
        self.resetScoreboard()
        supervisor.initializeSimulationState()
        supervisor.pauseSimulationExecution()
      else:
        self.initialTimeSeconds = self.timeRemain_s
        self.timeStepNormalizer = 0    
        print(f"{self.timeRemainMinutes} : {self.timeRemain_s}")

  def checkBall(self, supervisor):
    ballCoordinate = supervisor.fetchCurrentBallPosition()

    if abs(ballCoordinate[0]) > 4.5:
      if abs(ballCoordinate[1]) < 1.35:
        if supervisor.ballPriority == "N":
          if 4.5 < ballCoordinate[0]:
            print("RED GOAL!")
            self.redTeamScore += 1
            print(f"RED {self.redTeamScore} - {self.blueTeamScore} BLUE")
            supervisor.updateBallControlPriority("B")

          else:
            print("BLUE GOAL!")
            self.blueTeamScore += 1
            print(f"RED {self.redTeamScore} - {self.blueTeamScore} BLUE")
            supervisor.updateBallControlPriority("R")
        
          self.latestGoalTime = time.time() * 1000
          # print(self.latestGoalTime)

        if self.latestGoalTime < (time.time() * 1000) - 5000:
          # print(time.time() * 1000)
          supervisor.initializeSimulationState()

      else:
        if 4.5 < ballCoordinate[0]:
          supervisor.updateBallControlPriority("B")
          supervisor.updateBallPositionOnField(BALL_POSITIONS["OUT_B"])
        else:
          supervisor.updateBallControlPriority("R")
          supervisor.updateBallPositionOnField(BALL_POSITIONS["OUT_R"])
    
    elif abs(ballCoordinate[1]) > 3:

      if ballCoordinate[1] > 0:
        ballCoordinate[1] = 2.4
      else:
        ballCoordinate[1] = -2.4

      ballCoordinate[2] = 0.0798759
      supervisor.updateBallPositionOnField(ballCoordinate)