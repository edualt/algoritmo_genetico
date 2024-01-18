import matplotlib.pyplot as plt

def plot_population(poblacionActual, minimize):
  # ordena de mayor a menor
  poblacionActual.sort(key=lambda x: x[3], reverse=True)

  if minimize:
    best = poblacionActual[0]
    worst = poblacionActual[-1]
  else:
    best = poblacionActual[-1]
    worst = poblacionActual[0]

  average = sum([x[3] for x in poblacionActual]) / len(poblacionActual)

  rangox = [] #x
  aptitud = [] #y

  for x in poblacionActual:
    rangox.append(x[2])
    aptitud.append(x[3])

  # grafica la siguiente funcion 

  plt.scatter(rangox, aptitud)
  plt.scatter(best[2], best[3], color='green')
  plt.scatter(worst[2], worst[3], color='red')
  plt.scatter(average, average, color='yellow')
  plt.title("INDIVIDUOS")
  plt.show()