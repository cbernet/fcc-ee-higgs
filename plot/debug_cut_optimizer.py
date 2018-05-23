
from plotconfig_ZH_ll import *
from cut_optimizer import CutOptimizer

cutopt = CutOptimizer([ZH, ZZ, WW, ll], basecut='1', cuts=cuts)
cutopt.draw_marginal('zeds_m', 'cut_z_mass')
