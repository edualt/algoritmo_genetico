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
        expression = ((((x**3)/100) * sin(x)) + ((x**2) * cos(x)))
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
        
    def pruning(self):
        self.population.sort(key=lambda individual: individual[3], reverse=True)
        self.population = self.population[:self.max_population]
        
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
            self.pruning()

            self.generations.append(self.population.copy())

