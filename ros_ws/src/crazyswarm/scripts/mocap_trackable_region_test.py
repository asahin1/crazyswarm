"""Single CF: takeoff, follow absolute-coords waypoints, land."""

import numpy as np

from pycrazyswarm import Crazyswarm

X_MIN = -0.8
X_MAX = 1.5

Y_MIN = -0.7
Y_MAX = 0.8
Y_STEPS = 4

Z_MIN = 0.8
Z_MAX = 0.8
Z_STEPS = 1

LONG_DUR = 6.0
SHORT_DUR = 3.0

TAKEOFF_DURATION = 2.5
GOTO_DURATION = 3.0

def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cf = swarm.allcfs.crazyflies[0]

    # print(cf.initialPosition)
    cf.initialPosition = cf.position()
    # cf.initialPosition = np.array([-0.65, -1, 0])
    # print(cf.initialPosition)

    cf.takeoff(targetHeight=Z_MIN, duration=TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + 1.0)

    y_list = np.linspace(Y_MIN,Y_MAX,Y_STEPS)
    z_list = np.linspace(Z_MIN,Z_MAX,Z_STEPS)
    print("y steps: ",y_list)
    print("z steps: ",z_list)

    x_lims = [X_MIN,X_MAX]
    for k in np.linspace(Z_MIN,Z_MAX,Z_STEPS):
        for j in np.linspace(Y_MIN,Y_MAX,Y_STEPS):
            p = np.array([x_lims[0],j, k])
            GOTO_DURATION = SHORT_DUR
            cf.goTo(p, yaw=0.0, duration=GOTO_DURATION)
            timeHelper.sleep(GOTO_DURATION + 1.0)
            print(cf.position())
            p = np.array([x_lims[1],j, k])
            GOTO_DURATION = LONG_DUR
            cf.goTo(p, yaw=0.0, duration=GOTO_DURATION)
            timeHelper.sleep(GOTO_DURATION + 1.0)
            print(cf.position())
            x_lims.reverse()

    cf.land(targetHeight=0.05, duration=TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + 1.0)


if __name__ == "__main__":
    main()
