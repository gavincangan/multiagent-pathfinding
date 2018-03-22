#!/usr/bin/env python
from macros import *
import numpy as np
import random
import world
import grid_agent as ga

class Belief:
    def __init__(self, nrows, ncols):


    @staticmethod
    def gauss_update(mean1, var1, mean2, var2):
        new_mean = (mean1 * var2 + mean2 * var1)/(var1 + var2)
        new_var = 1/((1/var1) + (1/var2))
        return [new_mean, new_var]
