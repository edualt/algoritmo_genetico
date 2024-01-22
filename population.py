import matplotlib.pyplot as plt
import numpy as np

def plot_population(poblacionActual, minimize, range_, function):
  poblacionActual.sort(key=lambda x: x[3], reverse=True)

  if minimize:
    best = poblacionActual[0]
    worst = poblacionActual[-1]
  else:
    best = poblacionActual[-1]
    worst = poblacionActual[0]

  rangox = [] #x
  aptitud = [] #y

  for x in poblacionActual:
    rangox.append(x[2])
    aptitud.append(x[3])

  x = np.linspace(range_[0], range_[1], 1000)
  y = function(x)

  plt.plot(x, y, color='black', zorder=1)
  plt.scatter(rangox, aptitud)
  plt.scatter(best[2], best[3], color='green')
  plt.scatter(worst[2], worst[3], color='red')
  plt.title("INDIVIDUOS")
  plt.xlim(range_[0], range_[1])
  plt.show()