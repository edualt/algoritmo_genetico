import numpy as np
import matplotlib.pyplot as plt

def plot_population(poblacionActual):
  poblacionActual.sort(key=lambda individual: individual[2])  # Sorting by phenotype (x)
  fig, ax = plt.subplots()

  rangox = [] #x
  aptitud = [] #y

  for x in poblacionActual:
    rangox.append(x[2])
    aptitud.append(x[3])


  for a, b in zip(rangox, aptitud):
      plt.text(a, b, f"({round(a,4)}, {round(b,4)})")

  ax.plot(rangox, aptitud)  #Aqui cambiar datos de la grafica
  plt.scatter(rangox, aptitud)
  plt.title("INDIVIDUOS Y CURVA")
  plt.show()