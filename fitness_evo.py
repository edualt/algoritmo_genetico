import matplotlib.pyplot as plt

# realiza una diagrama de dispersión de la evolución de la aptitud
def plot_fitness_evolution(fitness_over_generations):
    print(fitness_over_generations)
    x = [i for i in range(len(fitness_over_generations))]
    plt.scatter(x, fitness_over_generations)
    plt.title("Evolución de la aptitud")
    plt.xlabel("Generación")
    plt.ylabel("Aptitud")
    plt.show()
