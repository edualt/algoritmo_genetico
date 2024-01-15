import numpy as np
import matplotlib.pyplot as plt

def plot_evolution(max_generations, best_cases, worst_cases, average_cases):
    plt.figure()
    plt.plot(np.arange(max_generations), [x[3] for x in best_cases], label="Best Cases")
    plt.plot(np.arange(max_generations), [x[3] for x in worst_cases], label="Worst Cases")
    plt.plot(np.arange(max_generations), average_cases, label="Average Cases")
    plt.legend()
    plt.title("Evolution")
    plt.xlabel("Generations")
    plt.ylabel("Fitness Value")
    plt.show()
