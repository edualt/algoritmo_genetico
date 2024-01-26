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
from utils import animarPlot, grabarVideo, unirVariosVideos, reproducirVideo
import time

class GeneticAlgorithm:
    def __init__(self, precision, range_, max_generations, max_population, initial_population_size, prob_mutation_gene, prob_mutation_individual, prob_crossover):
        x = symbols('x')
        # self.expression = sin(x)
        self.expression = (x * cos(x) * sin(2 * x) + (2 * x) )
        # expression = ((x ** 2) * cos(5 * x) - (3 * x))
        self.function = lambdify(x, simplify(self.expression))
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
        self.prob_crossover = prob_crossover
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
        unique_population = []
        seen_individuals = set()
        for individual in self.population:
            individual_tuple = tuple(individual[0])
            if individual_tuple not in seen_individuals:
                unique_population.append(individual)
                seen_individuals.add(individual_tuple)

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
    
    def get_elegible_to_crossover(self, population, prob_crossover):
        elegible = []
        for individual in population:
            if random.random() <= prob_crossover:
                elegible.append(individual)
        return elegible
            
    def start(self, minimize):
        self.generate_initial_population()
        generation = 0
        mejores = []
        while generation < self.max_generations:
            new_population = []
            elegible_to_crossover = self.get_elegible_to_crossover(self.population, self.prob_crossover)

            for _ in range(self.max_population - len(elegible_to_crossover)):
                parent_a = self.select_parent(self.population)
                parent_b = self.select_parent(self.population)
                child_a, child_b = self.crossover(parent_a, parent_b)
                child_a = self.mutation(child_a)
                child_b = self.mutation(child_b)
                new_population.append(child_a)
                new_population.append(child_b)
            
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

            x2 = np.linspace(self.range_[0], self.range_[1], 1000)
            y2 = self.function(x2)

            listaAnimaciones = []
            listaVideos = []
            inicio = time.time()
            for i in range(len(self.generations)):
                fig, animar = animarPlot(x,y)
                listaAnimaciones.append((fig,animar))
                listaVideos.append(f"video{i}.gif")
            unirVariosVideos(listaAnimaciones,listaVideos)
            fin = time.time()
            print(f"Tiempo de ejecución: {fin - inicio} segundos")

            fig, ax = plt.subplots()
            ax.scatter(x, y)
            plt.scatter(best[2], best[3], color='green')
            plt.scatter(worst[2], worst[3], color='red')
            plt.plot(x2, y2, color='black', zorder=1)
            plt.title(f"Generación {generation}")
            plt.xlabel("x")
            plt.ylabel("y")
            plt.xlim(self.range_[0], self.range_[1]) 
            plt.legend(['individuos', 'mejor',  'peor', 'f(x)'])
            plt.savefig(f"images/generation {generation}.png")
            plt.close()
            

