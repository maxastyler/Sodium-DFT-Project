#!/bin/python3

"""
This script has functions that can take in PT-Energy data from a quantum espresso output file and interpolate them using bicubic splines.
"""

import numpy as np
from scipy.interpolate import interp2d

