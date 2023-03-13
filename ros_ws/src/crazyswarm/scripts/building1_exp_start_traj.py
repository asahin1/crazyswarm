#!/usr/bin/env python

import numpy as np

from pycrazyswarm import *
import uav_trajectory

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    traj1 = uav_trajectory.Trajectory()
    traj1.loadcsv("my_trajectories/b1_traj1.csv")

    traj2 = uav_trajectory.Trajectory()
    traj2.loadcsv("my_trajectories/b1_traj2.csv")

    TRIALS = 1
    TIMESCALE = 1.0

    for i in range(TRIALS):
        for cf in allcfs.crazyflies:
            cf.uploadTrajectory(0, 0, traj1)
            cf.uploadTrajectory(1, 2, traj2)

        cf.initialPosition = cf.position()

        allcfs.takeoff(targetHeight=0.2, duration=2.0)
        timeHelper.sleep(2.5)
        for cf in allcfs.crazyflies:
            pos = np.array(cf.initialPosition) + np.array([0, 0, 0.2])
            cf.goTo(pos, 0, 2.0)
        timeHelper.sleep(2.5)

        allcfs.startTrajectory(0, timescale=TIMESCALE, relative=False)
        timeHelper.sleep(traj1.duration * TIMESCALE + 2.0)
        allcfs.startTrajectory(1, timescale=TIMESCALE, relative=False)
        timeHelper.sleep(traj1.duration * TIMESCALE + 2.0)

        allcfs.land(targetHeight=0.06, duration=2.0)
        timeHelper.sleep(3.0)
