# Blue Team Goalkeeper robot behaviours.

import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))  # 获取当前文件所在目录的路径
parentdir = os.path.dirname(currentdir)  # 获取当前文件所在目录的父目录路径
sys.path.append(parentdir)  # 将父目录路径添加到系统路径中，以便导入自定义模块

from Base.SoccerRobotBase import SoccerRobot  # 导入基础机器人类
from Utils import Functions  # 导入工具函数模块
from Utils.Consts import (TIME_STEP, Motions)  # 导入时间步长和动作常量

class Goalkeeper(SoccerRobot):
    # 在此定义了机器人运行时的行为逻辑
    def run(self):
        self.printSelf()  # 打印机器人信息
        flag = 0  # 定义标志变量
        flag1 = 0  # 定义标志变量
        flag2 = 0  # 定义标志变量
        flag3 = 0  # 定义标志变量
        fixedCoordinate = [4.22, -0.00114, 0.343]  # 固定坐标
        origin = [0, 0, 0]  # 原点坐标
        count_0 = 0  # 计数器
        count = 0  # 计数器
        count1 = 0  # 计数器
        while self.robot.step(TIME_STEP) != -1:  # 在时间步长内循环执行
            # 检查是否有新的球数据可用
            if self.isNewBallDataAvailable():
                self.getSupervisorData()  # 获取最新的监控数据
                # 获取球数据和自身坐标
                data = self.supervisorData
                ballOwner = self.getBallOwner()
                ballCoordinate = self.getBallData()
                blue_fw_l = [data[30], data[31], data[32]]  # 获取左侧蓝队前锋坐标
                blue_fw_r = [data[33], data[34], data[35]]  # 获取右侧蓝队前锋坐标
                redFw = [data[21], data[22], data[23]]  # 获取红队前锋坐标
                blueDef = [data[27], data[28], data[29]]  # 获取蓝队防守球员坐标
                selfCoordinate = self.getSelfCoordinate()  # 获取自身坐标
                # 检查球是否进了球门
                if self.checkGoal() == 1:
                    decidedMotion =  self.motions.handWave
                    # 检查新动作是否有效
                    if self.isNewMotionValid(decidedMotion):
                        boolean = self.currentlyMoving and \
                                  (self.currentlyMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                        if boolean:
                            self.interruptMotion()  # 中断当前动作
                        self.clearMotionQueue()  # 清空动作队列
                        if boolean:
                            self.addMotionToQueue(self.motions.standInit)  # 添加站立动作到队列
                        self.addMotionToQueue(decidedMotion)  # 添加手挥动作到队列
                    self.startMotion()  # 开始执行动作
                elif self.checkGoal() == -1:
                    decidedMotion =  self.motions.standInit
                    print('decidedMotion:', decidedMotion)
                    # 检查新动作是否有效
                    if self.isNewMotionValid(decidedMotion):
                        print('self.currentlyMoving:', self.currentlyMoving)
                        boolean = self.currentlyMoving and \
                                  (self.currentlyMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                        if boolean:
                        #     self.interruptMotion()  # 中断当前动作
                        # self.clearMotionQueue()  # 清空动作队列
                        # if boolean:
                        #     self.addMotionToQueue(self.motions.standInit)  # 添加站立动作到队列
                          self.addMotionToQueue(decidedMotion)  # 添加站立动作到队列
                          self.startMotion()  # 开始执行动作
                robotHeightFromGround = selfCoordinate[2]  # 获取机器人距离地面的高度
                # 检查机器人是否倒下
                if robotHeightFromGround < 0.2:
                    print('判断1')
                    if self.getLeftSonarValue() == 2.55 and self.getRightSonarValue() == 2.55:
                        decidedMotion = self.motions.standUpFromBack
                    else:
                        decidedMotion = self.motions.standUpFromFront
                    # 检查新动作是否有效
                    if self.isNewMotionValid(decidedMotion):
                        boolean = self.currentlyMoving and \
                                  (self.currentlyMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                        if boolean:
                            self.interruptMotion()  # 中断当前动作
                        self.clearMotionQueue()  # 清空动作队列
                        if boolean:
                            self.addMotionToQueue(self.motions.standInit)  # 添加站立动作到队列
                        self.addMotionToQueue(decidedMotion)  # 添加站立动作到队列
                    self.startMotion()  # 开始执行动作
                # 检查球是否在对方优势位置
                elif self.getBallPriority() == "R":
                    print('判断2')
                    decidedMotion = self.motions.standInit
                    # 检查新动作是否有效
                    if self.isNewMotionValid(decidedMotion):
                        boolean = self.currentlyMoving and \
                                  (self.currentlyMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                        if boolean:
                            self.interruptMotion()  # 中断当前动作
                        self.clearMotionQueue()  # 清空动作队列
                        if boolean:
                            self.addMotionToQueue(self.motions.standInit)  # 添加站立动作到队列
                        self.addMotionToQueue(decidedMotion)  # 添加站立动作到队列
                    self.startMotion()  # 开始执行动作
                else:
                    print('判断3')
                    print('selfCoordinate:', selfCoordinate[0], selfCoordinate[1])
                    print('ballCoordinate:', ballCoordinate[0], ballCoordinate[1])
                    if selfCoordinate[0] >= 3.56 and selfCoordinate[0] <= 4.44 and selfCoordinate[1] >= -1.47 and selfCoordinate[1] <= 1.47 and flag2 == 0:
                        if ballCoordinate[0] >= 3.4 and ballCoordinate[0] <= 4.44 and ballCoordinate[1] >= -1.5 and ballCoordinate[1] <= 1.5:
                            print('判断6')
                            flag = 1
                            decidedMotion = self.decideMotion(ballCoordinate, selfCoordinate, blue_fw_l, blue_fw_r, redFw, blueDef)
                            if count_0 >= 2:
                                decidedMotion = self.motions.rightShoot
                                count_0 = 0
                            if decidedMotion ==  self.motions.longShoot:
                                count_0 = count_0 + 1
                            # 检查新动作是否有效
                            if self.isNewMotionValid(decidedMotion):
                                boolean = self.currentlyMoving and \
                                        (self.currentlyMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                                if boolean:
                                    self.interruptMotion()  # 中断当前动作
                                self.clearMotionQueue()  # 清空动作队列
                                if boolean:
                                    self.addMotionToQueue(self.motions.standInit)  # 添加站立动作到队列
                                self.addMotionToQueue(decidedMotion)  # 添加站立动作到队列
                                self.startMotion()  # 开始执行动作
                        else:
                            print('判断5')
                            # if (ballCoordinate[0] <= 3.4 or ballCoordinate[0] >= 4.44) and flag == 1:
                            #     flag1 = 0
                            #     decidedMotion = self.returnMotion(fixedCoordinate, selfCoordinate)
                            #     # 检查新动作是否有效
                            #     if self.isNewMotionValid(decidedMotion):
                            #         boolean = self.currentlyMoving and \
                            #                 (self.currentlyMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                            #         if boolean:
                            #             self.interruptMotion()  # 中断当前动作
                            #         self.clearMotionQueue()  # 清空动作队列
                            #         if boolean:
                            #             self.addMotionToQueue(self.motions.standInit)  # 添加站立动作到队列
                            #         self.addMotionToQueue(decidedMotion)  # 添加站立动作到队列
                            #         self.startMotion()  # 开始执行动作
                            #         if (selfCoordinate[0] >= 4.0 and selfCoordinate[0] <= 4.5) and (selfCoordinate[1] >= -0.01 and selfCoordinate[1] <= 0):
                            #             flag = 0 
                            #             flag1 = 1 
                            # elif (ballCoordinate[0] <= 3.4 or ballCoordinate[0] >= 4.44) and flag == 0 and flag1 == 0:
                            #     decidedMotion = self.followBallDirection(ballCoordinate, selfCoordinate)
                            #     # 检查新动作是否有效
                            #     if self.isNewMotionValid(decidedMotion):
                            #         self.interruptMotion()  # 中断当前动作
                            #         self.clearMotionQueue()  # 清空动作队列
                            #         self.addMotionToQueue(decidedMotion)  # 添加动作到队列
                            #         self.startMotion()  # 开始执行动作
                            # elif flag1 == 1:
                            #     decidedMotion = self.turnMotion(origin, selfCoordinate)
                            #     if decidedMotion == self.motions.standInit:
                            #         count = count + 1
                            #     if count >= 2:
                            #         flag1 = 0
                            #         count = 0
                            #     # 检查新动作是否有效
                            #     if self.isNewMotionValid(decidedMotion):
                            #         boolean = self.currentlyMoving and \
                            #                 (self.currentlyMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                            #         if boolean:
                            #             self.interruptMotion()  # 中断当前动作
                            #         self.clearMotionQueue()  # 清空动作队列
                            #         if boolean:
                            #             self.addMotionToQueue(self.motions.standInit)  # 添加站立动作到队列
                            #         self.addMotionToQueue(decidedMotion)  # 添加站立动作到队列
                            #         self.startMotion()  # 开始执行动作
                            if (ballCoordinate[0] <= 3.4 or ballCoordinate[0] >= 4.44) and flag == 1:
                              print('-----------判断1---------')
                              # 如果球的x坐标小于等于3.4或大于等于4.44，并且flag等于1
                              flag1 = 0
                              decidedMotion = self.returnMotion(fixedCoordinate, selfCoordinate)
                              # 将标志flag1设置为0，并获取根据固定坐标和自身坐标返回的动作
                              # 检查新动作是否有效
                              print('decidedMotion:', decidedMotion.name)
                              print('self.currentlyMoving.name:', self.currentlyMoving.name)
                              if self.isNewMotionValid(decidedMotion):
                                  # 如果新动作有效
                                  boolean = self.currentlyMoving and \
                                            (self.currentlyMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                                  # 检查当前是否正在执行动作，且当前动作是向前50，并且新动作不是向前50
                                  # if boolean:
                                      # self.interruptMotion()  # 中断当前动作
                                      # self.clearMotionQueue()  # 清空动作队列
                                  print('boolean', boolean)
                                  if boolean:
                                      print('扑倒！！！！！')
                                      # self.addMotionToQueue(self.motions.standInit)  # 如果boolean为真，则将站立初始动作添加到队列
                                      self.addMotionToQueue(decidedMotion)  # 添加新动作到队列
                                      self.startMotion()  # 开始执行动作
                                  # if (selfCoordinate[0] >= 4.0 and selfCoordinate[0] <= 4.5) and (selfCoordinate[1] >= -0.01 and selfCoordinate[1] <= 0):
                                  #     flag = 0  # 如果自身坐标的范围满足条件，则将flag设置为0
                                  #     flag1 = 1  # 设置flag1为1
                              elif (ballCoordinate[0] <= 3.4 or ballCoordinate[0] >= 4.44) and flag == 0 and flag1 == 0:
                                  print('-----------判断2---------')
                                  # 如果球的x坐标小于等于3.4或大于等于4.44，并且flag等于0且flag1等于0
                                  decidedMotion = self.followBallDirection(ballCoordinate, selfCoordinate)
                                  # 根据球的坐标和自身坐标确定动作
                                  # 检查新动作是否有效
                                  if self.isNewMotionValid(decidedMotion):
                                      # 如果新动作有效
                                      self.interruptMotion()  # 中断当前动作
                                      self.clearMotionQueue()  # 清空动作队列
                                      self.addMotionToQueue(decidedMotion)  # 添加新动作到队列
                                      self.startMotion()  # 开始执行动作
                              elif flag1 == 1:
                                  print('-----------判断3---------')
                                  # 如果flag1等于1
                                  decidedMotion = self.turnMotion(origin, selfCoordinate)
                                  # 根据原点和自身坐标确定转动动作
                                  if decidedMotion == self.motions.standInit:
                                      count = count + 1  # 如果决定的动作是站立初始动作，则增加计数
                                  if count >= 2:
                                      flag1 = 0  # 如果计数大于等于2，则将flag1设置为0
                                      count = 0  # 重置计数
                                  # 检查新动作是否有效
                                  if self.isNewMotionValid(decidedMotion):
                                      # 如果新动作有效
                                      boolean = self.currentlyMoving and \
                                                (self.currentlyMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                                      # 检查当前是否正在执行动作，且当前动作是向前50，并且新动作不是向前50
                                      if boolean:
                                          self.interruptMotion()  # 中断当前动作
                                      self.clearMotionQueue()  # 清空动作队列
                                      if boolean:
                                          self.addMotionToQueue(self.motions.standInit)  # 如果boolean为真，则将站立初始动作添加到队列
                                      self.addMotionToQueue(decidedMotion)  # 添加新动作到队列
                                      self.startMotion()  # 开始执行动作

                    else:
                        print('判断4')
                        flag2 = 1
                        if flag3 == 0:
                            decidedMotion = self.returnMotion(fixedCoordinate, selfCoordinate)
                            # 检查新动作是否有效
                            if self.isNewMotionValid(decidedMotion):
                                boolean = self.currentlyMoving and \
                                        (self.currentlyMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                                if boolean:
                                    self.interruptMotion()  # 中断当前动作
                                self.clearMotionQueue()  # 清空动作队列
                                if boolean:
                                    self.addMotionToQueue(self.motions.standInit)  # 添加站立动作到队列
                                self.addMotionToQueue(decidedMotion)  # 添加站立动作到队列
                                self.startMotion()  # 开始执行动作
                                if (selfCoordinate[0] >= 4.0 and selfCoordinate[0] <= 4.5) and (selfCoordinate[1] >= -0.01 and selfCoordinate[1] <= 0):
                                    flag3 = 1
                        else:
                            decidedMotion = self.turnMotion(origin, selfCoordinate)
                            if decidedMotion == self.motions.standInit:
                                count1 = count1 + 1
                            if count1 >= 2:
                                flag2 = 0
                                flag3 = 0
                                count1 = 0
                            # 检查新动作是否有效
                            if self.isNewMotionValid(decidedMotion):
                                boolean = self.currentlyMoving and \
                                        (self.currentlyMoving.name == self.motions.forwards50.name and decidedMotion.name != self.motions.forwards50.name)
                                if boolean:
                                    self.interruptMotion()  # 中断当前动作
                                self.clearMotionQueue()  # 清空动作队列
                                if boolean:
                                    self.addMotionToQueue(self.motions.standInit)  # 添加站立动作到队列
                                self.addMotionToQueue(decidedMotion)  # 添加站立动作到队列
                                self.startMotion()  # 开始执行动作
            else:
                print("NO BALL DATA!!!")  # 输出无球数据提示

    # 重写 decideMotion 方法
    def decideMotion(self, ballCoordinate, selfCoordinate, blue_fw_l, blue_fw_r, redFw, blueDef):
        
        robotHeadingAngle = self.getRollPitchYaw()[2]  # 获取机器人的航向角
        turningAngle = Functions.calculateTurningAngleAccordingToRobotHeading(ballCoordinate, selfCoordinate, robotHeadingAngle)  # 计算机器人相对于球的转向角度
        if turningAngle > 50:
            return self.motions.turnLeft60
        elif turningAngle > 30:
            return self.motions.turnLeft40
        elif turningAngle < -50:
            return self.motions.turnRight60
        elif turningAngle < -30:
            return self.motions.turnRight40
        distanceFromBall = Functions.calculateDistance(ballCoordinate, selfCoordinate)  # 计算机器人与球之间的距离
        if distanceFromBall < 0.32:
            print('球来了')
            return self.motions.cartwheelBlock
            # if self.check_position(selfCoordinate, redFw):  # 检查是否在红队前锋位置
            #     if redFw[1] > 0:
            #         return self.motions.rightSidePass
            #     elif selfCoordinate[1] > redFw[1]:
            #         return self.motions.longShoot
            #     else:
            #         return self.motions.leftSidePass
            # else:
            #     return self.pass_motion(selfCoordinate, blue_fw_l, blue_fw_r, redFw, blueDef)  # 传球动作
        return self.motions.forwards50
    
    # 返回动作
    def returnMotion(self, ballCoordinate, selfCoordinate):
        robotHeadingAngle = self.getRollPitchYaw()[2]
        turningAngle = Functions.calculateTurningAngleAccordingToRobotHeading(ballCoordinate, selfCoordinate, robotHeadingAngle)
        print(turningAngle)
        if turningAngle > 50:
            # return self.motions.turnLeft60
            return self.motions.cartwheelBlock
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
        turningAngle = Functions.calculateTurningAngleAccordingToRobotHeading(ballCoordinate, selfCoordinate, robotHeadingAngle)
        if turningAngle > 50:
            return self.motions.turnLeft60
        elif turningAngle > 30:
            return self.motions.turnLeft40
        elif turningAngle < -50:
            return self.motions.turnRight60
        elif turningAngle < -30:
            return self.motions.turnRight40
        return self.motions.standInit
    
    # 跟随球运动
    def followBallDirection(self, ballCoordinate, selfCoordinate):
        robotHeadingAngle = self.getRollPitchYaw()[2]
        turningAngle = Functions.calculateTurningAngleAccordingToRobotHeading(ballCoordinate, selfCoordinate, robotHeadingAngle)
        if turningAngle > 50:
            return self.motions.sideStepLeft
        elif turningAngle > 30:
            return self.motions.sideStepLeft
        elif turningAngle < -50:
            return self.motions.sideStepRight
        elif turningAngle < -30:
            return self.motions.sideStepRight
        else:
            return self.motions.standInit

    # 检查位置
    def check_position(self, selfCoordinate, redForward):
        if redForward[0] >= 3.4 and redForward[0] <= 4.4 and redForward[1] >= -1.5 and redForward[1] <= 1.5:
            return True
        else:
            return False 
    
    # 传球动作
    def pass_motion(self, selfCoordinate, blue_fw_l, blue_fw_r, redFw, blueDef):
        robotHeadingAngle = self.getRollPitchYaw()[2]
        turningAngle = Functions.calculateTurningAngleAccordingToRobotHeading(blueDef, selfCoordinate, robotHeadingAngle)
        if turningAngle <-50:
            print('defender left side pass -50')
            return self.motions.leftSidePass
        elif turningAngle <-30:       
            print('defender left side pass -30')
            return self.motions.leftSidePass
        else:
            print('in long pass')
            return self.motions.longShoot  
