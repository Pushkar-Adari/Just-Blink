import matplotlib.pyplot as plt
from matplotlib.pyplot import plt, savefig

import numpy as np

plt.style.use('theme.mplstyle')

x_data = np.arange(0,50,0.1)
y_data = np.sin(x_data)
y_data2 = np.cos(x_data)

plt.plot(x_data,y_data,color = "red")
plt.plot(x_data,y_data2,color="yellow")
plt.show()
plt.savefig('your_figure.png', transparent=True)
