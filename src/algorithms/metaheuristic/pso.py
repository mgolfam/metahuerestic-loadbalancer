import random
import numpy as np
from src.algorithms.metaheuristic.metaheuristic_abstract import Metaheuristic
from src.cloud.task import Task

class ParticleSwarmOptimization(Metaheuristic):
    """
    Particle Swarm Optimization (PSO) Algorithm for task-to-VM allocation optimization.
    """

    def __init__(self, config):
        """
        Initializes the PSO algorithm.

        Args:
            config (dict): Configuration dictionary with algorithm-specific parameters.
        """
        super().__init__(config)
        self.num_particles = config.get("num_particles", 100)
        self.inertia_weight = config.get("inertia_weight", 0.5)
        self.cognitive_weight = config.get("cognitive_weight", 1.5)
        self.social_weight = config.get("social_weight", 1.5)
        self.best_fitness = []

    def initialize_population(self, tasks, vms):
        """
        Initializes a population of particles (task-to-VM allocations).

        Args:
            tasks (list): List of CPU utilization tasks.
            vms (list): List of VMs with their free CPU capacities.

        Returns:
            list: Initial population of task-to-VM allocations and velocities.
        """
        population = []
        velocities = []
        for _ in range(self.num_particles):
            allocation = np.random.choice(range(len(vms)), size=len(tasks))
            velocity = np.zeros_like(allocation)  # Initialize velocity to zero
            population.append(allocation)
            velocities.append(velocity)
        return population, velocities

    def evaluate_fitness(self, population, tasks, vms):
        """
        Evaluates the fitness of each particle in the population.

        Args:
            population (list): List of particle allocations.
            tasks (list): List of CPU utilization tasks.
            vms (list): List of VMs with their free CPU capacities.

        Returns:
            list: Fitness scores for each particle.
        """
        fitness_scores = []
        for allocation in population:
            vm_loads = [0] * len(vms)
            for task, vm_idx in zip(tasks, allocation):
                vm_loads[vm_idx] += task

            # Calculate fitness: Penalize overloaded VMs
            overload_penalty = sum(
                max(0, load - vms[vm_idx].free_cpu_percent() * vms[vm_idx].cpu_core)
                for vm_idx, load in enumerate(vm_loads)
            )
            fitness = -overload_penalty  # Minimize overload
            fitness_scores.append(fitness)
        return fitness_scores

    def update_population(self, population, velocities, fitness_scores, best_positions, tasks, vms):
        """
        Updates the population based on fitness scores and particle velocities.

        Args:
            population (list): List of particle allocations.
            velocities (list): List of particle velocities.
            fitness_scores (list): Fitness scores of the population.
            best_positions (list): Best position for each particle.
        """
        global_best_position = max(zip(fitness_scores, population), key=lambda x: x[0])[1]
        for i in range(len(population)):
            # Update particle velocity
            r1 = np.random.rand(len(population[i]))
            r2 = np.random.rand(len(population[i]))

            velocities[i] = (
                self.inertia_weight * velocities[i] +
                self.cognitive_weight * r1 * (best_positions[i] - population[i]) +
                self.social_weight * r2 * (global_best_position - population[i])
            )

            # Update particle position (task-to-VM allocation)
            population[i] += velocities[i].astype(int)
            population[i] = np.clip(population[i], 0, len(vms) - 1)  # Ensure positions are valid

        # Update the best positions for each particle
        for i in range(len(population)):
            if fitness_scores[i] > self.evaluate_fitness([best_positions[i]], tasks, vms)[0]:
                best_positions[i] = population[i]

    def optimize(self, tasks, vms):
        """
        Runs the PSO algorithm to optimize task allocation.

        Args:
            tasks (list): List of CPU utilization tasks.
            vms (list): List of VMs with their free CPU capacities.

        Returns:
            list: Optimized task-to-VM mapping.
        """
        population, velocities = self.initialize_population(tasks, vms)
        best_positions = population[:]  # Initial best positions are the same as the population

        for _ in range(self.config.get("iterations", 50)):
            fitness_scores = self.evaluate_fitness(population, tasks, vms)
            self.update_population(population, velocities, fitness_scores, best_positions, tasks, vms)

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
        plt.title("PSO Algorithm's Convergence")
        plt.show()
