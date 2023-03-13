#!/usr/bin/env python

import numpy as np
from pycrazyswarm import *

Z = 0.3

if __name__ == "__main__":
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    allcfs.takeoff(targetHeight=Z, duration=1.0+Z)
    timeHelper.sleep(1.5+Z*10)
    for cf in allcfs.crazyflies:
        pos = np.array([0, 0, Z]) + np.array([0, 0, Z])
        # Alternatively, use this
        # pos = cf.position() + np.array([0, 0, Z])
        cf.goTo(pos, 0, 1.0)

    print("press button to continue...")
    swarm.input.waitUntilButtonPressed()

    allcfs.land(targetHeight=0.02, duration=1.0+Z)
    timeHelper.sleep(1.0+Z)
