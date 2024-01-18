import tkinter as tk
from tkinter import ttk
from algoritmo_genetico import GeneticAlgorithm, plot_evolution, plot_population
from tkinter import messagebox


root = tk.Tk()
root.geometry("700x500")     
root.title('Genetic Algorithm')
root.configure(bg="black")


label_x_position = 50
entry_x_position = 250
y_position = 50
y_increment = 30


title_label = ttk.Label(root, text="Parameters for the Algorithm", background='red', font=('Input Mono.', '12', 'bold')).place(x=250, y=10)

max_x_label = ttk.Label(root, text="Maximum Value of X:", background='red', font=('Input Mono.', '10')).place(x=label_x_position, y=y_position)
max_x_entry = ttk.Entry(root)
max_x_entry.insert(0, "4")
max_x_entry.place(x=entry_x_position, y=y_position)

y_position += y_increment
min_x_label = ttk.Label(root, text="Minimum Value of X:", background='red', font=('Input Mono.', '10')).place(x=label_x_position, y=y_position)
min_x_entry = ttk.Entry(root)
min_x_entry.insert(0, "-4")
min_x_entry.place(x=entry_x_position, y=y_position)

y_position += y_increment
resolution_x_label = ttk.Label(root, text="Precision for X:", background='red', font=('Input Mono.', '10')).place(x=label_x_position, y=y_position)
resolution_x_entry = ttk.Entry(root)
resolution_x_entry.insert(0, "0.05")
resolution_x_entry.place(x=entry_x_position, y=y_position)

y_position += y_increment
max_generation_label = ttk.Label(root, text="Maximum Generations", background='red', font=('Input Mono.', '10')).place(x=label_x_position, y=y_position)
max_generation_entry = ttk.Entry(root)
max_generation_entry.insert(0, "10")
max_generation_entry.place(x=entry_x_position, y=y_position)

y_position += y_increment
initial_population_label = ttk.Label(root, text="Initial Population", background='red', font=('Input Mono.', '10')).place(x=label_x_position, y=y_position)
initial_population_entry = ttk.Entry(root)
initial_population_entry.insert(0, "3")
initial_population_entry.place(x=entry_x_position, y=y_position)

y_position += y_increment
max_population_label = ttk.Label(root, text="Maximum Population:", background='red', font=('Input Mono.', '10')).place(x=label_x_position, y=y_position)
max_population_entry = ttk.Entry(root)
max_population_entry.insert(0, "10")
max_population_entry.place(x=entry_x_position, y=y_position)

y_position += y_increment
individual_mutation_label = ttk.Label(root, text="Pmi", background='red', font=('Input Mono.', '10')).place(x=label_x_position, y=y_position)
individual_mutation_entry = ttk.Entry(root)
individual_mutation_entry.insert(0, "0.7")
individual_mutation_entry.place(x=entry_x_position, y=y_position)

y_position += y_increment
gen_mutation_prob_label = ttk.Label(root, text="Pmg", background='red', font=('Input Mono.', '10')).place(x=label_x_position, y=y_position)
gen_mutation_prob_entry = ttk.Entry(root)
gen_mutation_prob_entry.insert(0, "0.25")
gen_mutation_prob_entry.place(x=entry_x_position, y=y_position)

y_position += y_increment
crossover_prob_label = ttk.Label(root, text="Crossover Probability (Pc):", background='red', font=('Input Mono.', '10')).place(x=label_x_position, y=y_position)
crossover_prob_entry = ttk.Entry(root)
crossover_prob_entry.insert(0, "0.8")
crossover_prob_entry.place(x=entry_x_position, y=y_position)



# Botones
y_position += y_increment
maximize_button = ttk.Button(root, text="Maximize X", command=lambda: run(True)).place(x=250, y=y_position)
minimize_button = ttk.Button(root, text="Minimize X", command=lambda: run(False)).place(x=350, y=y_position)

def run(minimize: bool):
  ga = GeneticAlgorithm(float(resolution_x_entry.get()), (float(min_x_entry.get()), float(max_x_entry.get())), int(max_generation_entry.get()), int(max_population_entry.get()), int(initial_population_entry.get()), float(individual_mutation_entry.get()), float(gen_mutation_prob_entry.get()))
  ga.start(minimize)

  plot_evolution(ga.max_generations, ga.best_cases, ga.worst_cases, ga.average_cases)
  # print(ga.generations[-1])
  plot_population(ga.generations[-1], minimize)

  messagebox.showinfo(message=f"Genotype: {ga.population[0][0]}\ni: {ga.population[0][1]}, Phenotype: {ga.population[0][2]}, Fitness: {ga.population[0][3]}", title="Best Individual")

root.mainloop()