from matplotlib import pyplot as plt



plt.figure()
plt.plot([1.1,2.2,3.3,4.4], [5.5,6.6,7.7,8.8], 'r-*')
plt.plot([4],[4], 'bo')
plt.xlabel("Number of ...") 
plt.ylabel("Chance to win")

plt.figure()
for x in range(10):
    y = x**2 
    if y % 2 == 0: # Modulo check for even number
        plt.plot([x], [y], 'r*')
    else:
        plt.plot([x], [y], 'k*')

    plt.xlabel("X")
    plt.ylabel("X squared")

plt.figure()
plt.bar([1,2,3,4],[1,4,9,16])
plt.xlabel("X")
plt.ylabel("X squared")

plt.show()
