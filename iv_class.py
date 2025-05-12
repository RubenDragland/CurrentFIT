import numpy as np
import torch
from torchmin import minimize, Minimizer
import os
from cost_function_classes import (
    SphericalHarmonicsObjective,
    EXPSIN2Objective,
    CostFunctionSAXSTT,
    EXPSIN1Objective,
)
from optimisers import OptimiserSAXSTT
import scipy.io
from SAXSTT_functionality import reshape_projections, reshape_fortran
import time
from os import path
from scipy.special import sph_harm
from scipy.integrate import simpson

# Idea overhead that is initialised, loads data and sets up the model, calls optimisation.


