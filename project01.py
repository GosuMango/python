import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0,2,100)

plt.figure(figsize=(7,7), layout='constrained')# Create a figure containing a single Axes.
plt.plot(x, x, label='linear')  # Plot some data on the (implicit) Axes.
plt.plot(x, x**2, label='quadratic')  # etc.
plt.plot(x, x**6, label='cubic')
plt.xlabel('x label')
plt.ylabel('y label')
plt.title("Simple Plot")
plt.show()