'''
motion planning.py
Author: Jeremy (Jiajie) He <jiajiehe@stanford.edu>
Created: 2/10/2018
'''

import numpy as np
import matplotlib.pyplot as plt

'''
function: build_grid
inputs:
	rows: int
	columns: int
	goal_row: int
	goal_col: int
	start_row: int
	start_column: int
	num_obstacle: int
outputs:
	grid: numpy.array
description:
	each node in this grid has a reward (namely the value of each entry in this grid)
	the destination node has a great positive reward (e.g. 100)
	the obstacles have great negative rewards (e.g. -100)
	the obstacles are generated randomly
	there is no obstacle withn a certain area around the destination and starting point
'''
def build_grid(rows, columns, goal_row, goal_col, start_row, start_col, num_obstacle):
	grid = np.zeros((rows,columns))
	grid[goal_row, goal_col] = 100
	i = 0
	while i < num_obstacle:
		obstacle_row = np.random.randint(0, rows - 1)
		obstacle_col = np.random.randint(0, columns - 1)
		if ( (obstacle_row - goal_row)**2 + (obstacle_col - goal_col)**2 ) > 4 and ( (obstacle_row - start_row)**2 + (obstacle_col - start_col)**2 ) > 4 :
			grid[obstacle_row, obstacle_col] = -100
			i += 1
	return grid

'''
function: compute_path
inputs:
	rows: int
	columns: int
	grid: np.array
	iterations: int
	gamma: float
	actions: dict
description:
	best_action: dict
	state_utility: dict
'''
def compute_path(rows, columns, grid, iterations, gamma, actions):
	state_utility = {}
	best_action = {}
	for i in range(iterations):
		for row in range(rows):
			for col in range(columns):
				if row == goal_row and col == goal_col:
					state_utility[(row, col)] = 100
				else:
					max_utility = -100
					for key, value in actions.iteritems():
						next_row = row + value[0]
						next_col = col + value[1]
						if 0 <= next_row < rows and 0 <= next_col < columns:
							utility = grid[row, col] + gamma * state_utility.get((next_row, next_col), 0)
							if utility >= max_utility:
								max_utility = utility
								best_action[(row, col)] = key
					state_utility[(row, col)] = max_utility
	return best_action, state_utility

'''
function: plot_utility
inputs:
	state_utility: dict
outputs:
	a plot of utility values of all states (all nodes in the grid)
'''
def plot_utility(state_utility):
	plt.figure()
	utility_grid = np.zeros((rows,columns))
	for key, value in state_utility.iteritems():
		utility_grid[key[0],key[1]] = value
	plt.imshow(utility_grid)
	plt.show()

'''
function: plot_path
inputs:
	goal_row: int
	goal_col: int 
	start_row: int 
	start_col: int 
	actions: dict 
	best_action:dict
outputs:
	a plot of utility values of all states (all nodes in the grid)
'''
def plot_path(goal_row, goal_col, start_row, start_col, actions, best_action):
	plt.figure()
	plt.imshow(grid)
	i = 0
	current_row = start_row
	current_col = start_col
	while (current_row != goal_row) or (current_col != goal_col):
		print("step = %d" % i)
		print("current_row = %d" % current_row)
		print("current_col = %d" % current_col)
		step = actions[best_action[(current_row, current_col)]]
		next_row = current_row + step[0]
		next_col = current_col + step[1]
		plt.plot([current_col, next_col], [current_row, next_row], 'w')
		current_row = next_row
		current_col = next_col
		i += 1
	plt.show()

#####################################################
#Change the the parameters in the following function#
#####################################################
if __name__ == "__main__":
	'''
	Change the following parameters
		rows: number of rows in this grid
		columns: number of columns in this grid
		goal_row: the row index of destination (0 <= goal_row < rows)
		goal_col: the column index of destination (0 <= goal_col < columns)
		start_row: the row index of starting point (0 <= start_row < rows)
		start_column: the column index of starting point (0 <= start_col < columns)
		num_obstacle: number of obstacles
		gamma: discount factor
		iterations: times of value iteration
	'''
	#################################
	#Change the following parameters#
	#################################
	rows = 30
	columns = 30
	goal_row = 28 # 0-indexing
	goal_col = 2 # 0-indexing
	start_row = 3 # 0-indexing
	start_col = 26 # 0-indexing
	num_obstacle = 300 
	gamma = 0.95
	iterations = 50
	#################################

	actions = {'up':(0, 1), 'down':(0, -1), 'left':(-1, 0), 'right':(1, 0)}

	grid = build_grid(rows, columns, goal_row, goal_col, start_row, start_col, num_obstacle)

	best_action, state_utility = compute_path(rows, columns, grid, iterations, gamma, actions)
	
	#plot_utility(state_utility)

	plot_path(goal_row, goal_col, start_row, start_col, actions, best_action)
