from matplotlib import pyplot as plt
import math

x = 0 # m
y = 0 # m
g = 9.82 # m/s^2

angle = float(input("Enter launch angle in degrees: "))
angle_rad = math.radians(angle)

v0 = float(input("Enter initial speed in m/s: ")) # initial speed in m/s

vx = v0 * math.cos(angle_rad) # m/s
vy = v0 * math.sin(angle_rad) # m/s

dt= 0.001 # detla time, time step
xs=[] # list of x positions
ys=[] # list of y positions
t = 0 # total time

while y >= 0:
    xs.append(x)
    ys.append(y)
    t = t + dt
    x = x + vx*dt
    y = y + vy*dt
    vy = vy - g*dt 

print(f"Landing distance: {x:.2f} m")
print(f"Flight time: {t:.2f} s")

plt.plot(xs,ys, 'b-*')
plt.title('Projectile Motion')
plt.xlabel('Distance (m)')
plt.ylabel('Height (m)')
plt.show()