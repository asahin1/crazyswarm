"""Single CF: takeoff, follow absolute-coords waypoints, land."""

import numpy as np

from pycrazyswarm import Crazyswarm


Z = 0.5
TAKEOFF_DURATION = 2.5
GOTO_DURATION = 3.0

# Square waypoints
# WAYPOINTS = np.array([
#     (0.2, 0.0, Z),
#     (0.2, -0.2, Z),
#     (-0.6, -0.2, Z),
#     (-0.6, 0.0, Z),
#     (0.0, 0.0, Z)
# ])

# Square waypoints with altitude shift
# WAYPOINTS = np.array([
#     (0.2, 0.0, Z+0.3),
#     (0.2, -0.2, Z-0.2),
#     (-0.6, -0.2, Z+0.3),
#     (-0.6, 0.0, Z-0.2),
#     (0.0, 0.0, Z)
# ])

# For local mocap tests
WAYPOINTS = np.array([
    (0.6, 0.0, Z),
    (-0.6, 0.0, Z),
    (0.6, 0.0, Z)
])


def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cf = swarm.allcfs.crazyflies[0]

    # print(cf.initialPosition)
    cf.initialPosition = cf.position()
    # print(cf.initialPosition)

    cf.takeoff(targetHeight=Z, duration=TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + 1.0)

    for p in WAYPOINTS:
        cf.goTo(cf.initialPosition + p, yaw=0.0, duration=GOTO_DURATION)
        timeHelper.sleep(GOTO_DURATION + 1.0)
        print(cf.position())

    cf.land(targetHeight=0.05, duration=TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + 1.0)


if __name__ == "__main__":
    main()
