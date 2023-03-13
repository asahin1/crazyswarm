#!/usr/bin/env python

import numpy as np

from pycrazyswarm import *
import uav_trajectory


def executeTrajectory(timeHelper, cf, trajpath, rate=100, offset=np.zeros(3)):
    traj = uav_trajectory.Trajectory()
    traj.loadcsv(trajpath)

    start_time = timeHelper.time()
    while not timeHelper.isShutdown():
        t = timeHelper.time() - start_time
        if t > traj.duration:
            break

        e = traj.eval(t)
        # print("e.pos: ",e.pos)
        # print("cf.position()",cf.position())
        # if (e.pos[2] < 0.2):
        #     print("Passing too close to the ground!")
        cf.cmdFullState(
            e.pos + offset,
            e.vel,
            e.acc,
            e.yaw,
            e.omega)

        timeHelper.sleepForRate(rate)

    hover_start = timeHelper.time()
    hover_duration = 3
    while not timeHelper.isShutdown():
        t = timeHelper.time() - hover_start
        if t > hover_duration:
            break
        cf.cmdFullState(e.pos + offset, np.zeros(3), np.zeros(3), 0, np.zeros(3))
        timeHelper.sleepForRate(rate)


if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cf = swarm.allcfs.crazyflies[0]

    # cf.initialPosition = np.array([0.55, -0.5, 0.0])
    cf.initialPosition = cf.position()

    rate = 30.0
    Z = 0.3

    timeHelper.sleep(10)

    cf.takeoff(targetHeight=Z, duration=Z+1.0)
    timeHelper.sleep(Z+2.0)

    # executeTrajectory(timeHelper, cf, "my_trajectories/traj_square.csv", rate, offset=np.array([0, 0, 0.0]))
    executeTrajectory(timeHelper, cf, "my_trajectories/b1_cf3_traj1.csv", rate, offset=np.array([0, 0, 0.0]))
    timeHelper.sleepForRate(30)
    executeTrajectory(timeHelper, cf, "my_trajectories/b1_cf3_traj2.csv", rate, offset=np.array([0, 0, 0.0]))

    cf.notifySetpointsStop()
    cf.land(targetHeight=0.03, duration=Z+1.0)
    timeHelper.sleep(Z+2.0)
