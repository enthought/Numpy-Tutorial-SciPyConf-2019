""" Run this file to check your python installation.
"""
import numpy as np
import matplotlib.pyplot as plt

assert np.allclose(np.array([3.3], dtype='float32'), np.array([1.65], dtype='float32')*2)
fig, ax = plt.subplots()
ax.scatter(x=[-3, -2, -1, 0, 1, 2, 3], y=[0, -1, -1.5, -1.75, -1.5, -1, 0])
ax.scatter(x=[-1.5, 1.5], y=[2, 2], s=1000)
ax.set_ylim((-3, 3))
plt.show()
