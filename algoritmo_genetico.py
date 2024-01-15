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


