#from matplotlib import pyplot as plt
import random, math

#plt.figure()
n_in_circle = 0
n_out_circle = 0
run_times=1_000_000_0

for i in range(run_times):
    """
    Pi = 4*Area_circle/area_square
    square sides are 2*r
    circle radius is r
    """
    x = random.uniform(-1,1)
    y = random.uniform(-1,1)
    d = math.sqrt(x**2 + y**2)
    if d > 1:
        #plt.plot([x], [y], 'r*')
        n_out_circle += 1
    else:
        #plt.plot([x], [y], 'b*')
        n_in_circle += 1

    #plt.xlabel("X")
    #plt.ylabel("X squared")

#plt.show()

# print the closest approximation of pi
a=run_times
print(f"Out of {a} runs {n_out_circle} were out of circle and {n_in_circle} were in the circle")

# find estimate of pi
est_pi = 4 * n_in_circle / run_times
print(f"Estimate of pi: {est_pi:.20f}")
# A faster version without plotting
"""
import random
import time
s=time.time
n_in_circle = 0
run_times = 1_000_000  # increase for more decimals

for _ in range(run_times):
    x = random.random() * 2 - 1   # [-1,1]
    y = random.random() * 2 - 1
    if x*x + y*y <= 1:            # faster than sqrt
        n_in_circle += 1

est_pi = 4 * n_in_circle / run_times
print(f"Estimate of pi: {est_pi:.20f}")
"""