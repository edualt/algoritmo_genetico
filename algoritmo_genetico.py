import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox
import random
import math
from sympy import lambdify, simplify, sin, cos, symbols
from statistics import mean
from grafica import plot_evolution
from population import plot_population

class GeneticAlgorithm:
    def __init__(self, precision, range_, max_generations, max_population, initial_population_size, prob_mutation_gene, prob_mutation_individual):
        x = symbols('x')
        expression = sin(x)
        # expression = (x * cos(x) * sin(2 * x) + (2 * x) )
        # expression = ((x ** 2) * cos(5 * x) - (3 * x))
        self.function = lambdify(x, simplify(expression))
        self.precision = precision
        self.range_ = range_
        self.max_population = max_population
        self.initial_population_size = initial_population_size
        self.max_generations = max_generations
        self.rx = self.range_[1] - self.range_[0]
        self.n_px = math.ceil(self.rx / self.precision) + 1
        self.n_bx = len(bin(self.n_px)) - 2
        self.population = []
        self.best_cases = []
        self.worst_cases = []
        self.average_cases = []
        self.prob_mutation_individual = prob_mutation_individual
        self.prob_mutation_gene = prob_mutation_gene
        self.generations = []
        
    def mutation(self, individual):
        if random.random() <= self.prob_mutation_individual:
            for i in range(self.n_bx):
                if random.random() <= self.prob_mutation_gene:
                    individual[0][i] = 1 - individual[0][i]
            return self.create_individual(individual[0])
        return individual
        
    def create_individual(self, genotype):
        i = int("".join(map(str, genotype)), 2)
        phenotype = self.range_[0] + i * self.precision
        phenotype = min(phenotype, self.range_[1])
        fitness = self.function(phenotype)
        return [genotype, i, phenotype, fitness]
        
    def pruning(self, minimize):
        # Eliminar individuos duplicados
        unique_population = []
        seen_individuals = set()
        for individual in self.population:
            individual_tuple = tuple(individual[0])
            if individual_tuple not in seen_individuals:
                unique_population.append(individual)
                seen_individuals.add(individual_tuple)

        # Ordenar y realizar la poda
        unique_population.sort(key=lambda x: x[3], reverse=minimize)
        self.population = unique_population[:self.max_population]
        
    def crossover(self, a, b):
        crossover_point = random.randint(1, self.n_bx - 1)
        genotype_a = a[0][:crossover_point] + b[0][crossover_point:]
        genotype_b = b[0][:crossover_point] + a[0][crossover_point:]
        return self.create_individual(genotype_a), self.create_individual(genotype_b)

    @staticmethod
    def select_parent(population):
        return random.choice(population)
        
    def generate_initial_population(self):
        for _ in range(self.initial_population_size):
            genotype = [random.getrandbits(1) for _ in range(self.n_bx)]
            individual = self.create_individual(genotype)
            self.population.append(individual)
            
    def start(self, minimize):
        mejores = self.population[:self.initial_population_size] 
        
        generation = 0
        self.generate_initial_population()
        
        for _ in range(self.max_generations):
            new_population = []
            for _ in range(len(self.population) // 2):
                parent_a = self.select_parent(self.population)
                parent_b = self.select_parent(self.population)
                child_a, child_b = self.crossover(parent_a, parent_b)
                new_population.append(self.mutation(child_a))
                new_population.append(self.mutation(child_b))
            
            self.population.extend(new_population)
            self.population.sort(key=lambda x: x[3], reverse=minimize)
            self.best_cases.append(self.population[0])
            self.worst_cases.append(self.population[-1])
            self.average_cases.append(mean(x[3] for x in self.population))

            self.generations.append(self.population.copy())

            if len(self.population) > self.max_population:
                self.pruning(minimize)
                
            generation += 1
            x = []
            y = []
            for individual in self.population:
                x.append(individual[2])
                y.append(individual[3])

            # Create a list of tuples from x and y
            points = list(zip(x, y))

            # Sort the list of tuples by the x values
            points.sort(key=lambda point: point[0])

            # Unzip the list of tuples
            x, y = zip(*points)

            # crea una copia de la poblacion
            population_copy = self.population.copy()
            population_copy.sort(key=lambda x: x[3], reverse=True)

            if minimize:
                best = population_copy[0]
                worst = population_copy[-1]
            else:
                best = population_copy[-1]
                worst = population_copy[0]

            self.population[-self.initial_population_size:] = mejores
            mejores = self.population[:self.initial_population_size]

            fig, ax = plt.subplots()
            ax.scatter(x, y)
            ax.plot(x, y, color="black")
            plt.scatter(best[2], best[3], color='green')
            plt.scatter(worst[2], worst[3], color='red')
            plt.title(f"Generación {generation}")
            plt.xlabel("x")
            plt.ylabel("y")
            plt.xlim(self.range_[0], self.range_[1]) 
            plt.savefig(f"images/generation {generation}.png")
            
            

