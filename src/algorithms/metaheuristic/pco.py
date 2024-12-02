import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.algorithms.metaheuristic.metaheuristic_abstract import Metaheuristic
from src.cloud.task import Task

class PlantCompetitionOptimization(Metaheuristic):
    """
    Plant Competition Optimization (PCO) Algorithm for CPU utilization.
    """

    def __init__(self, config):
        """
        Initializes the PCO algorithm.

        Args:
            config (dict): Configuration dictionary with algorithm-specific parameters.
        """
        super().__init__(config)
        self.max_plant_number = config.get("max_plant_number", 1000)
        self.k = config.get("k", 0.1)
        self.teta = np.exp(-1)
        self.best_fitness = []

    def initialize_population(self, tasks, vms):
        """
        Initializes a population of plants (VM allocation to hosts).

        Args:
            tasks (list): List of CPU utilization tasks.
            vms (list): List of VMs with their free CPU capacities.

        Returns:
            list: Initial population of task-to-VM allocations.
        """
        population = []
        for _ in range(self.config["num_plants"]):
            allocation = np.random.choice(range(len(vms)), size=len(tasks))
            population.append(allocation)
        return population

    def evaluate_fitness(self, population, tasks, vms):
        """
        Evaluates the fitness of each allocation.

        Args:
            population (list): List of task-to-VM allocations.
            tasks (list): List of CPU utilization tasks.
            vms (list): List of VM objects with their free CPU capacities.

        Returns:
            list: Fitness scores for each allocation.
        """
        fitness_scores = []
        for allocation in population:
            vm_loads = [0] * len(vms)
            for task, vm_idx in zip(tasks, allocation):
                vm_loads[vm_idx] += task

            # Calculate fitness: Penalize overloaded VMs
            overload_penalty = sum(
                max(0, load - vms[vm_idx].free_cpu_percent() * vms[vm_idx].cpu_core)  # Correctly calculate free CPU
                for vm_idx, load in enumerate(vm_loads)
            )
            fitness = -overload_penalty  # Minimize overload
            fitness_scores.append(fitness)
        return fitness_scores

    def update_population(self, population, fitness_scores, vms):
        """
        Updates the plant population by selecting and mutating top-performing allocations.

        Args:
            population (list): List of task-to-VM allocations.
            fitness_scores (list): Fitness scores of the allocations.
        """
        # Ensure fitness_scores are scalar and not numpy arrays
        fitness_scores = [float(score) for score in fitness_scores]

        # Select top-performing allocations
        sorted_population = [x for _, x in sorted(zip(fitness_scores, population), key=lambda pair: pair[0], reverse=True)]
        top_population = sorted_population[: len(sorted_population) // 2]

        # Reproduce and mutate
        while len(top_population) < len(population):
            parent = random.choice(top_population)
            offspring = parent[:]
            mutate_idx = np.random.randint(len(parent))
            offspring[mutate_idx] = np.random.randint(len(vms))  # Mutate task-to-VM mapping
            top_population.append(offspring)

        # Update population
        population[:] = top_population


    def optimize(self, tasks, vms):
        """
        Runs the PCO algorithm to optimize task allocation.

        Args:
            tasks (list): List of CPU utilization tasks.
            vms (list): List of VMs with their free CPU capacities.

        Returns:
            list: Optimized task-to-VM mapping.
        """
        population = self.initialize_population(tasks, vms)
        for iteration in range(self.config.get("iterations", 50)):
            fitness_scores = self.evaluate_fitness(population, tasks, vms)
            self.update_population(population, fitness_scores, vms)

            # Track best fitness
            best_fitness = max(fitness_scores)
            self.best_fitness.append(best_fitness)

        # Return the best solution
        best_solution_idx = np.argmax(fitness_scores)
        return population[best_solution_idx]

    def plot_convergence(self):
        """
        Plots the convergence of the algorithm.
        """
        plt.plot(self.best_fitness, 'b*-', linewidth=1, markeredgecolor='r', markersize=5)
        plt.xlabel('Iteration')
        plt.ylabel('Fitness Value')
        plt.title("PCO Algorithm's Convergence")
        plt.show()
