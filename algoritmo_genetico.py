import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox
import random
import math
from sympy import lambdify, simplify, sin, cos, symbols 
from statistics import mean

class GeneticAlgorithm:
    def __init__(self, precision, range_, maxGenerations, maxPopulation, initialPopulationSize, probMutationGene, probMutationIndividual):
        x = symbols('x')
        expression = (sin(x))
        self.function = lambdify(x, simplify(expression))
        self.precision = precision
        self.range_ = range_
        self.maxPopulation = maxPopulation
        self.initialPopulationSize = initialPopulationSize
        self.maxGenerations = maxGenerations
        self.Rx = self.range_[1] - self.range_[0]
        self.nPx = math.ceil(self.Rx / self.precision) + 1
        self.nBx = len(bin(self.nPx)) - 2
        self.population = []
        self.bestCases = []
        self.worstCases = []
        self.averageCases = []
        self.probMutationIndividual = probMutationIndividual
        self.probMutationGene = probMutationGene
        
    def mutation(self, individual):
        if random.random() <= self.probMutationIndividual: 
            for i in range(self.nBx):
                if random.random() <= self.probMutationGene:
                    individual[0][i] = 1 - individual[0][i]
            return self.createIndividual(individual[0])
        return individual
        
    def createIndividual(self, genotype):
        i = int("".join(map(str, genotype)), 2)
        phenotype = self.range_[0] + i * self.precision
        phenotype = min(phenotype, self.range_[1])
        fitness = self.function(phenotype)
        return [genotype, i, phenotype, fitness]
        
    def pruning(self):
        self.population.sort(key=lambda individual: individual[3], reverse=True)
        self.population = self.population[:self.maxPopulation]
        
    def crossover(self, a, b):
        crossoverPoint = random.randint(1, self.nBx - 1)
        genotypeA = a[0][:crossoverPoint] + b[0][crossoverPoint:]
        genotypeB = b[0][:crossoverPoint] + a[0][crossoverPoint:]
        return self.createIndividual(genotypeA), self.createIndividual(genotypeB)

    @staticmethod
    def selectParent(population):
        return random.choice(population)
        
    def generateInitialPopulation(self):
        for _ in range(self.initialPopulationSize):
            genotype = random.choices([0, 1], k=self.nBx)
            individual = self.createIndividual(genotype)
            self.population.append(individual)
            
    def start(self, minimize):
        self.generateInitialPopulation()
        for _ in range(self.maxGenerations):
            newPopulation = []
            for _ in range(len(self.population) // 2):
                parent1 = self.selectParent(self.population)
                parent2 = self.selectParent(self.population)
                child1, child2 = self.crossover(parent1, parent2)
                newPopulation.extend([self.mutation(child1), self.mutation(child2)])
            self.population.extend(newPopulation)
            self.population.sort(key=lambda x: x[3], reverse=minimize)
            self.bestCases.append(self.population[0])
            self.worstCases.append(self.population[-1])
            self.averageCases.append(mean(x[3] for x in self.population))
            self.pruning()


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
max_x_entry.insert(0, "2")
max_x_entry.place(x=entry_x_position, y=y_position)

y_position += y_increment
min_x_label = ttk.Label(root, text="Minimum Value of X:", background='red', font=('Input Mono.', '10')).place(x=label_x_position, y=y_position)
min_x_entry = ttk.Entry(root)
min_x_entry.insert(0, "-5")
min_x_entry.place(x=entry_x_position, y=y_position)

y_position += y_increment
resolution_x_label = ttk.Label(root, text="Precision for X:", background='red', font=('Input Mono.', '10')).place(x=label_x_position, y=y_position)
resolution_x_entry = ttk.Entry(root)
resolution_x_entry.insert(0, "0.5")
resolution_x_entry.place(x=entry_x_position, y=y_position)

y_position += y_increment
max_generation_label = ttk.Label(root, text="Maximum Generations", background='red', font=('Input Mono.', '10')).place(x=label_x_position, y=y_position)
max_generation_entry = ttk.Entry(root)
max_generation_entry.insert(0, "100")
max_generation_entry.place(x=entry_x_position, y=y_position)

y_position += y_increment
initial_population_label = ttk.Label(root, text="Initial Population", background='red', font=('Input Mono.', '10')).place(x=label_x_position, y=y_position)
initial_population_entry = ttk.Entry(root)
initial_population_entry.insert(0, "10")
initial_population_entry.place(x=entry_x_position, y=y_position)

y_position += y_increment
max_population_label = ttk.Label(root, text="Maximum Population:", background='red', font=('Input Mono.', '10')).place(x=label_x_position, y=y_position)
max_population_entry = ttk.Entry(root)
max_population_entry.insert(0, "100")
max_population_entry.place(x=entry_x_position, y=y_position)

y_position += y_increment
individual_mutation_label = ttk.Label(root, text="Pmi", background='red', font=('Input Mono.', '10')).place(x=label_x_position, y=y_position)
individual_mutation_entry = ttk.Entry(root)
individual_mutation_entry.insert(0, "0.7")
individual_mutation_entry.place(x=entry_x_position, y=y_position)

y_position += y_increment
gen_mutation_prob_label = ttk.Label(root, text="Pmg", background='red', font=('Input Mono.', '10')).place(x=label_x_position, y=y_position)
gen_mutation_prob_entry = ttk.Entry(root)
gen_mutation_prob_entry.insert(0, "0.6")
gen_mutation_prob_entry.place(x=entry_x_position, y=y_position)

y_position += y_increment
crossover_prob_label = ttk.Label(root, text="Crossover Probability (Pc):", background='red', font=('Input Mono.', '10')).place(x=label_x_position, y=y_position)
crossover_prob_entry = ttk.Entry(root)
crossover_prob_entry.insert(0, "0.5")
crossover_prob_entry.place(x=entry_x_position, y=y_position)

y_position += y_increment
elitism_size_label = ttk.Label(root, text="Elitism Size:", background='red', font=('Input Mono.', '10')).place(x=label_x_position, y=y_position)
elitism_size_entry = ttk.Entry(root)
elitism_size_entry.insert(0, "5")
elitism_size_entry.place(x=entry_x_position, y=y_position)

# Botones
y_position += y_increment
maximize_button = ttk.Button(root, text="Maximize X", command=lambda: run(True)).place(x=250, y=y_position)
minimize_button = ttk.Button(root, text="Minimize X", command=lambda: run(False)).place(x=350, y=y_position)

# Function to run algorithm and display results
def run(minimize: bool):
    ga = GeneticAlgorithm(float(resolution_x_entry.get()), (float(min_x_entry.get()), float(max_x_entry.get())), int(max_generation_entry.get()), int(max_population_entry.get()), int(initial_population_entry.get()), float(individual_mutation_entry.get()), float(gen_mutation_prob_entry.get()))
    ga.start(minimize)
    
    # Results
    plt.figure()
    plt.plot(np.arange(ga.maxGenerations), [x[3] for x in ga.bestCases], label="Best Cases")
    plt.plot(np.arange(ga.maxGenerations), [x[3] for x in ga.worstCases], label="Worst Cases")
    plt.plot(np.arange(ga.maxGenerations), ga.averageCases, label="Average Cases")
    plt.legend()
    plt.title("Evolution")
    plt.xlabel("Generations")
    plt.ylabel("Fitness Value")
    plt.show()
    
    # Message
    messagebox.showinfo(message=f"Genotype: {ga.population[0][0]}\ni: {ga.population[0][1]}, Phenotype: {ga.population[0][2]}, Fitness: {ga.population[0][3]}", title="Best Individual")
    

root.mainloop()
