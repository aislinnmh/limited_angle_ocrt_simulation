import numpy as np
import pykonal # requires cython, h5py, numpy, scipy, and pykonal install
from matplotlib import pyplot as plt

# Instantiate EikonalSolver object using Cartesian coordinates.
solver = pykonal.EikonalSolver(coord_sys="cartesian")
# Set the coordinates of the lower bounds of the computational grid.
# For Cartesian coordinates this is x_min, y_min, z_min.
# In this example, the origin is the lower bound of the computation grid.
solver.velocity.min_coords = 0,0,0
# Set the interval between nodes of the computational grid.
# For Cartesian coordinates this is dx, dy, dz.
# In this example the nodes are separated by 1 km in in each direction.
solver.velocity.node_intervals = 1,1,1
# Set the number of nodes in the computational grid.
# For Cartesian coordinates this is nx, ny, nz.
# This is a 2D example, so we only want one node in the z direction.
x = 8
y = 8
solver.velocity.npts = x,y,1
# Set the velocity model.
# In this case the velocity is equale to 1 km/s everywhere.
v = np.zeros(solver.velocity.npts) 
# print(v.shape)
for j in range(x):
    v[3,j] = 1
    v[2,j] = 0.1
    v[4,j] = 0.1

v[3,4] = 0.1
solver.velocity.values = v
print(v)

# Initialize the source. This is the trickiest part of the example.
# The source coincides with the node at index (0, 0, 0)
src_idx = 3, 0, 0

# Set the traveltime at the source node to 0.
solver.traveltime.values[src_idx] = 0
# Set the unknown flag for the source node to False.
# This is an FMM state variable indicating which values are completely
# unknown. Setting it to False indicates that the node has a tentative value
# assigned to it. In this case, the tentative value happens to be the true,
# final value.
solver.unknown[src_idx] = False
# Push the index of the source node onto the narrow-band heap.
solver.trial.push(*src_idx)

# Solve the system.
solver.solve()

# And finally, get the traveltime values.
# print(solver.traveltime.values)

tt = solver.traveltime.values


plt.figure(1)
plt.scatter(np.transpose(np.tile(range(8),(8,1))),np.tile(range(8),(8,1)),c=np.reshape(np.squeeze(tt),(8, 8)))
plt.colorbar()
plt.show()

