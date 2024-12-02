import numpy as np
from src.algorithms.metaheuristic.metaheuristic_abstract import Metaheuristic
from src.cloud.task import Task

class GrayWolfOptimization(Metaheuristic):
    """
    Gray Wolf Optimization (GWO) Algorithm for task-to-VM allocation optimization.
    """

    def __init__(self, config):
        """
        Initializes the GWO algorithm.

        Args:
            config (dict): Configuration dictionary with algorithm-specific parameters.
        """
        super().__init__(config)
        self.num_wolves = config.get("num_wolves", 100)
        self.a_max = config.get("a_max", 2)  # Linearly decreasing parameter
        self.best_fitness = []

    def initialize_population(self, tasks, vms):
        """
        Initializes the population of gray wolves (task-to-VM allocations).

        Args:
            tasks (list): List of CPU utilization tasks.
            vms (list): List of VMs with their free CPU capacities.

        Returns:
            list: Initial population of task-to-VM allocations.
        """
        population = []
        for _ in range(self.num_wolves):
            allocation = np.random.choice(range(len(vms)), size=len(tasks))
            population.append(allocation)
        return population

    def evaluate_fitness(self, population, tasks, vms):
        """
        Evaluates the fitness of each wolf in the population.

        Args:
            population (list): List of wolf allocations.
            tasks (list): List of CPU utilization tasks.
            vms (list): List of VMs with their free CPU capacities.

        Returns:
            list: Fitness scores for each wolf.
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

    def update_population(self, population, fitness_scores, tasks, vms, iteration, max_iterations):
        """
        Updates the population based on the positions of alpha, beta, and delta wolves.

        Args:
            population (list): List of wolf allocations.
            fitness_scores (list): Fitness scores of the population.
            tasks (list): List of CPU utilization tasks.
            vms (list): List of VMs with their free CPU capacities.
            iteration (int): Current iteration number.
            max_iterations (int): Total number of iterations.
        """
        # Identify alpha, beta, and delta wolves
        sorted_indices = np.argsort(fitness_scores)[::-1]
        alpha, beta, delta = (population[sorted_indices[0]], 
                              population[sorted_indices[1]], 
                              population[sorted_indices[2]])

        a = self.a_max * (1 - iteration / max_iterations)  # Linearly decreasing parameter

        for i in range(len(population)):
            wolf = population[i]
            updated_wolf = np.zeros_like(wolf)

            for d in range(len(wolf)):
                # Compute attraction toward alpha
                r1, r2 = np.random.rand(), np.random.rand()
                A1 = 2 * a * r1 - a
                C1 = 2 * r2
                D_alpha = abs(C1 * alpha[d] - wolf[d])
                X1 = alpha[d] - A1 * D_alpha

                # Compute attraction toward beta
                r1, r2 = np.random.rand(), np.random.rand()
                A2 = 2 * a * r1 - a
                C2 = 2 * r2
                D_beta = abs(C2 * beta[d] - wolf[d])
                X2 = beta[d] - A2 * D_beta

                # Compute attraction toward delta
                r1, r2 = np.random.rand(), np.random.rand()
                A3 = 2 * a * r1 - a
                C3 = 2 * r2
                D_delta = abs(C3 * delta[d] - wolf[d])
                X3 = delta[d] - A3 * D_delta

                # Update position based on average
                updated_wolf[d] = (X1 + X2 + X3) / 3

            # Clip to valid task-to-VM allocations
            updated_wolf = np.clip(updated_wolf.astype(int), 0, len(vms) - 1)
            population[i] = updated_wolf

    def optimize(self, tasks, vms):
        """
        Runs the GWO algorithm to optimize task allocation.

        Args:
            tasks (list): List of CPU utilization tasks.
            vms (list): List of VMs with their free CPU capacities.

        Returns:
            list: Optimized task-to-VM mapping.
        """
        population = self.initialize_population(tasks, vms)
        max_iterations = self.config.get("iterations", 50)

        for iteration in range(max_iterations):
            fitness_scores = self.evaluate_fitness(population, tasks, vms)
            self.update_population(population, fitness_scores, tasks, vms, iteration, max_iterations)

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
        plt.title("GWO Algorithm's Convergence")
        plt.show()
