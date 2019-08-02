# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 20:28:17 2018

@author: Alexandre
"""

###############################################################################
import numpy as np
###############################################################################
from pyro.dynamic  import cartpole
from pyro.control  import nonlinear
from pyro.planning import randomtree
###############################################################################


sys  = cartpole.RotatingCartPole()

###############################################################################

x_start = np.array([0,-3.14,0,0])
x_goal  = np.array([0,0,0,0])

planner = randomtree.RRT( sys , x_start )

t = 50
    
planner.u_options = [
        np.array([-t,0]),
        np.array([ 0,0]),
        np.array([+t,0])
        ]

planner.goal_radius          = 1.5
planner.dt                   = 0.05
planner.max_nodes            = 5000
planner.max_solution_time    = 2.0
planner.max_distance_compute = 1000

planner.dyna_plot            = False

planner.find_path_to_goal( x_goal )

planner.plot_tree()

###############################################################################

planner.save_solution('fullyactuatedcartpole_rrt')

#planner.plot_open_loop_solution()
sys.animate_simulation(1.0,True)

###############################################################################

# Controller

traj = planner.trajectory

ctl  = nonlinear.ComputedTorqueController( sys , traj )

ctl.w0   = 1.0
ctl.zeta = 0.7

# goal
ctl.rbar = np.array([0,0])


# New cl-dynamic
cl_sys = ctl + sys

# Simultation
cl_sys.plot_phase_plane_trajectory( x_start  )
cl_sys.sim.plot('xu')
cl_sys.animate_simulation(1.2,True)