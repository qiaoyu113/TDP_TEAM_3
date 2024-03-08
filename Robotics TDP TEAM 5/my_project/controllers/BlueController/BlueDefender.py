"""
Blue Team Defender robot behaviours.
"""

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Base.SoccerRobotBase import SoccerRobot
from Utils import Functions
from Utils.Consts import (TIME_STEP, Motions)
from controller import Supervisor

class Defender(SoccerRobot):
    # 机器人运行主函数
    def run(self):
        self.printSelf()  # 打印机器人信息
        count_0 = 0
        flag = 0
        flag1 = 0
        fixedCoordinate = [-3.1, -0.00573, 0.342]  # 固定坐标
        origin = [0.0723, -0.0798, 0.0799]  # 原点坐标
        goto_Coordinate = [0, 0, 0]  # 前往坐标
        while self.robot.step(TIME_STEP) != -1:  # 当模拟未结束时循环执行

            if self.isNewBallDataAvailable():  # 如果有新的球数据可用
                self.getSupervisorData()  # 获取监视器数据
                data = self.supervisorData  # 使用球数据（位置）执行某些操作
                ballOwner = self.getBallOwner()  # 获取持球者
                ballCoordinate = self.getBallData()  # 获取球的数据
                blue_fw_l = [data[30], data[31], data[32]]  # 左前蓝队员坐标
                blue_fw_r = [data[33], data[34], data[35]]  # 右前蓝队员坐标
                redFw = [data[21], data[22], data[23]]  # 红队前锋坐标

                # 获取自身坐标
                selfCoordinate = self.getSelfCoordinate()

                # 检查进球情况以平衡机器人
                if self.checkGoal() == 1:
                    decidedMotion = self.motions.handWave
                    # 检查新动作是否有效
                    if self.isNewMotionValid(decidedMotion):
                        boolean = self.currentlyMoving and \
                                  (self.currentlyMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                        if boolean:
                            self.interruptMotion()
                        self.clearMotionQueue()
                        if boolean:
                            self.addMotionToQueue(self.motions.standInit)
                        self.addMotionToQueue(decidedMotion)
                        self.startMotion()

                elif self.checkGoal() == -1:
                    decidedMotion = self.motions.standInit
                    # 检查新动作是否有效
                    if self.isNewMotionValid(decidedMotion):
                        boolean = self.currentlyMoving and \
                                  (self.currentlyMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                        if boolean:
                            self.interruptMotion()
                        self.clearMotionQueue()
                        if boolean:
                            self.addMotionToQueue(self.motions.standInit)
                        self.addMotionToQueue(decidedMotion)
                        self.startMotion()

                # 检查机器人是否倒下
                robotHeightFromGround = selfCoordinate[2]
                if robotHeightFromGround < 0.2:
                    if self.getLeftSonarValue() == 2.55 and self.getRightSonarValue() == 2.55:
                        decidedMotion = self.motions.standUpFromBack
                    else:
                        decidedMotion = self.motions.standUpFromFront
                    # 检查新动作是否有效
                    if self.isNewMotionValid(decidedMotion):
                        boolean = self.currentlyMoving and \
                                  (self.currentlyMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                        if boolean:
                            self.interruptMotion()
                        self.clearMotionQueue()
                        if boolean:
                            self.addMotionToQueue(self.motions.standInit)
                        self.addMotionToQueue(decidedMotion)
                        self.startMotion()

                # 检查对手是否有球优先权
                elif self.getBallPriority() == "R":
                    decidedMotion = self.motions.standInit
                    # 检查新动作是否有效
                    if self.isNewMotionValid(decidedMotion):
                        boolean = self.currentlyMoving and \
                                  (self.currentlyMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                        if boolean:
                            self.interruptMotion()
                        self.clearMotionQueue()
                        if boolean:
                            self.addMotionToQueue(self.motions.standInit)
                        self.addMotionToQueue(decidedMotion)
                        self.startMotion()

                # 仅在禁区内接近球
                else:
                    if ballCoordinate[0] >= 2.54 and ballCoordinate[0] <= 4.44:
                        flag = 1
                        if ballCoordinate[1] >= -1.5 and ballCoordinate[1] <= 1.5 and (
                                ballOwner == 'BLUE_GK' or ballOwner[0] == 'R'):
                            # print('going to designated coordinates')
                            goto_Coordinate[0] = 4.22
                            goto_Coordinate[1] = -0.22
                            goto_Coordinate[2] = 0.315
                            decidedMotion = self.decideMotion(ballCoordinate, selfCoordinate, blue_fw_l, blue_fw_r,
                                                              redFw)  # print("RedForward - decidedMotion: ", decidedMotion.Name)

                            if self.isNewMotionValid(decidedMotion):
                                boolean = self.currentlyMoving and \
                                          (self.currentlyMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                                if boolean:
                                    self.interruptMotion()
                                self.clearMotionQueue()
                                if boolean:
                                    self.addMotionToQueue(self.motions.standInit)
                                self.addMotionToQueue(decidedMotion)

                            self.startMotion()
                        else:
                            decidedMotion = self.decideMotion(ballCoordinate, selfCoordinate, blue_fw_l, blue_fw_r,
                                                              redFw)
                            if count_0 >= 2:
                                decidedMotion = self.motions.rightShoot
                                count_0 = 0
                            if decidedMotion == self.motions.longShoot:
                                count_0 = count_0 + 1

                            if self.isNewMotionValid(decidedMotion):
                                boolean = self.currentlyMoving and \
                                          (self.currentlyMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                                if boolean:
                                    self.interruptMotion()
                                self.clearMotionQueue()
                                if boolean:
                                    self.addMotionToQueue(self.motions.standInit)
                                self.addMotionToQueue(decidedMotion)

                            self.startMotion()

                    else:
                        if (ballCoordinate[0] <= 2.54 or ballCoordinate[0] >= 4.44) and flag == 1:
                            flag1 = 0
                            decidedMotion = self.returnMotion(fixedCoordinate, selfCoordinate)
                            if self.isNewMotionValid(decidedMotion):
                                boolean = self.currentlyMoving and \
                                          (self.currentlyMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                                if boolean:
                                    self.interruptMotion()
                                self.clearMotionQueue()
                                if boolean:
                                    self.addMotionToQueue(self.motions.standInit)
                                self.addMotionToQueue(decidedMotion)

                            self.startMotion()
                            if (selfCoordinate[0] >= 2.8 and selfCoordinate[0] <= 3.2) and (
                                    selfCoordinate[1] >= -0.03 and selfCoordinate[1] <= 0):
                                flag = 0
                                flag1 = 1

                        if flag1 == 1:
                            decidedMotion = self.turnMotion(origin, selfCoordinate)
                            if self.isNewMotionValid(decidedMotion):
                                boolean = self.currentlyMoving and \
                                          (self.currentlyMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                                if boolean:
                                    self.interruptMotion()
                                self.clearMotionQueue()
                                if boolean:
                                    self.addMotionToQueue(self.motions.standInit)
                                self.addMotionToQueue(decidedMotion)

                            self.startMotion()

            else:
                print("NO BALL DATA!!!")

    # 确定动作
    def decideMotion(self, ballCoordinate, selfCoordinate, blue_fw_l, blue_fw_r, redFw):
        robotHeadingAngle = self.getRollPitchYaw()[2]
        turningAngle = Functions.calculateTurningAngleAccordingToRobotHeading(ballCoordinate, selfCoordinate,
                                                                              robotHeadingAngle)

        if turningAngle > 50:
            return self.motions.turnLeft60
        elif turningAngle > 30:
            return self.motions.turnLeft40
        elif turningAngle < -50:
            return self.motions.turnRight60
        elif turningAngle < -30:
            return self.motions.turnRight40

        distanceFromBall = Functions.calculateDistance(ballCoordinate, selfCoordinate)

        if distanceFromBall < 0.22:
            return self.passBall(selfCoordinate, blue_fw_l, blue_fw_r, redFw)

        return self.motions.forwards50

    # 返回动作
    def returnMotion(self, ballCoordinate, selfCoordinate):
        robotHeadingAngle = self.getRollPitchYaw()[2]
        turningAngle = Functions.calculateTurningAngleAccordingToRobotHeading(ballCoordinate, selfCoordinate,
                                                                              robotHeadingAngle)

        if turningAngle > 90:
            return self.motions.turnLeft180
        elif turningAngle > 50:
            return self.motions.turnLeft60
        elif turningAngle > 30:
            return self.motions.turnLeft40
        elif turningAngle < -50:
            return self.motions.turnRight60
        elif turningAngle < -30:
            return self.motions.turnRight40

        return self.motions.forwards50

    # 转向动作
    def turnMotion(self, ballCoordinate, selfCoordinate):
        robotHeadingAngle = self.getRollPitchYaw()[2]
        turningAngle = Functions.calculateTurningAngleAccordingToRobotHeading(ballCoordinate, selfCoordinate,
                                                                              robotHeadingAngle)

        if turningAngle > 90:
            return self.motions.turnLeft180
        elif turningAngle > 50:
            return self.motions.turnLeft60
        elif turningAngle > 30:
            return self.motions.turnLeft40
        elif turningAngle < -50:
            return self.motions.turnRight60
        elif turningAngle < -30:
            return self.motions.turnRight40

        return self.motions.standInit

    # 传球动作
    def passBall(self, selfCoordinate, blue_fw_l, blue_fw_r, redFw):
        if ((redFw[0] >= (blue_fw_l[0] - 0.5) and redFw[0] < blue_fw_l[0]) or (
                redFw[1] >= (blue_fw_l[1] - 0.45) and redFw[1] < blue_fw_l[1]) or (
                redFw[0] <= (blue_fw_l[0] + 0.5) and redFw[0] > blue_fw_l[0]) or (
                redFw[1] <= (blue_fw_l[1] + 0.45) and redFw[1] > blue_fw_l[1])):
            return self.pass_to_right(selfCoordinate, blue_fw_r)
        else:
            return self.pass_to_left(selfCoordinate, blue_fw_l)

    # 向右传球
    def pass_to_right(self, selfCoordinate, rightForward):
        robotHeadingAngle = self.getRollPitchYaw()[2]
        turningAngle = Functions.calculateTurningAngleAccordingToRobotHeading(rightForward, selfCoordinate,
                                                                              robotHeadingAngle)
        if turningAngle > 90:
            return self.motions.rightSidePass
        elif turningAngle > 50:
            return self.motions.rightSidePass
        elif turningAngle > 30:
            return self.motions.rightSidePass
        elif turningAngle < -50:
            return self.motions.leftSidePass
        elif turningAngle < -30:
            return self.motions.leftSidePass
        else:
            return self.motions.longShoot

    # 向左传球
    def pass_to_left(self, selfCoordinate, leftForward):
        robotHeadingAngle = self.getRollPitchYaw()[2]
        turningAngle = Functions.calculateTurningAngleAccordingToRobotHeading(leftForward, selfCoordinate,
                                                                              robotHeadingAngle)
        if turningAngle > 90:
            return self.motions.rightSidePass
        elif turningAngle > 50:
            return self.motions.rightSidePass
        elif turningAngle > 30:
            return self.motions.rightSidePass
        elif turningAngle < -50:
            return self.motions.leftSidePass
        elif turningAngle < -30:
            return self.motions.leftSidePass
        else:
            return self.motions.longShoot  
