#!/usr/bin/env python

import numpy as np
import csv

from pycrazyswarm import *
import uav_trajectory
import time


abs_start_time = 0
pos_log = []
time_log = []


def executeTrajectory(timeHelper, cf, trajpath, rate=100, offset=np.zeros(3)):
    traj = uav_trajectory.Trajectory()
    traj.loadcsv(trajpath)

    start_time = timeHelper.time()
    while not timeHelper.isShutdown():
        pos_log.append(cf.position())
        time_log.append(timeHelper.time()-abs_start_time);
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
        pos_log.append(cf.position())
        time_log.append(timeHelper.time()-abs_start_time);
        t = timeHelper.time() - hover_start
        if t > hover_duration:
            break
        cf.cmdFullState(e.pos + offset, np.zeros(3), np.zeros(3), 0, np.zeros(3))
        timeHelper.sleepForRate(rate)


if __name__ == "__main__":

    scenario = "b"

    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cf = swarm.allcfs.crazyflies[0]

    # cf.initialPosition = np.array([0.55, -0.5, 0.0])
    cf.initialPosition = cf.position()

    rate = 30.0
    Z = 0.3

    timeHelper.sleep(20)

    abs_start_time = timeHelper.time()
    cf.takeoff(targetHeight=Z, duration=Z+1.0)
    timeHelper.sleep(Z+2.0)

    if(scenario == "a"):
        executeTrajectory(timeHelper, cf, "my_trajectories/b1_inf5_p1_traj1_combined.csv", rate, offset=np.array([0, 0, 0.0]))
        timeHelper.sleepForRate(30)
        executeTrajectory(timeHelper, cf, "my_trajectories/b1_inf5_p1_traj2_combined.csv", rate, offset=np.array([0, 0, 0.0]))
    elif(scenario == "b"):
        executeTrajectory(timeHelper, cf, "my_trajectories/b1_inf5_p2_traj1_combined.csv", rate, offset=np.array([0, 0, 0.0]))
        timeHelper.sleepForRate(30)
        executeTrajectory(timeHelper, cf, "my_trajectories/b1_inf5_p2_traj2_combined.csv", rate, offset=np.array([0, 0, 0.0]))
    else:
        print("No scenario specified")
        timeHelper.sleepForRate(30)

    cf.notifySetpointsStop()
    cf.land(targetHeight=0.03, duration=Z+1.0)
    timeHelper.sleep(Z+2.0)


    timestr = time.strftime("%Y%m%d_%H%M%S")
    file_name = "trajectory_log/pos_log_" + timestr + ".csv"

    with open(file_name, 'w', newline='') as csvfile:
        log_writer = csv.writer(csvfile, delimiter=',')
        for i in range(0,len(pos_log)):
            log_writer.writerow([time_log[i],pos_log[i][0],pos_log[i][1],pos_log[i][2]])
