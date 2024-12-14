import numpy as np
from src.algorithms.metaheuristic.metaheuristic_abstract import Metaheuristic

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
        self.a_max = config.get("a_max", 2)
        self.max_iterations = config.get("iterations", 50)
        self.convergence_threshold = config.get("convergence_threshold", 1e-6)

    def initialize_population(self, tasks, vms):
        """
        Initializes the population of wolves (task-to-VM allocations).

        Args:
            tasks (list): List of tasks.
            vms (list): List of VMs.

        Returns:
            np.ndarray: Initial population as a matrix of size (num_wolves, len(tasks)).
        """
        return np.random.randint(0, len(vms), size=(self.num_wolves, len(tasks)))

    def evaluate_fitness(self, population, tasks, vms):
        """
        Evaluates the fitness of the population.

        Args:
            population (np.ndarray): Current population of wolves.
            tasks (list): List of tasks.
            vms (list): List of VMs.

        Returns:
            np.ndarray: Fitness values for the population.
        """
        fitness_scores = []
        for allocation in population:
            vm_utilization = [0] * len(vms)

            # Calculate VM utilization
            for task_idx, vm_idx in enumerate(allocation):
                task_cpu = tasks[task_idx] if isinstance(tasks[task_idx], (int, float)) else tasks[task_idx].cpu
                vm_utilization[vm_idx] += task_cpu

            # Penalize overloaded VMs
            overload_penalty = sum(
                max(0, util - vms[vm_idx].free_cpu_percent() * vms[vm_idx].cpu_core)
                for vm_idx, util in enumerate(vm_utilization)
            )

            # Load balance penalty
            ideal_load = sum(vm_utilization) / len(vms)
            load_balance_penalty = sum((util - ideal_load) ** 2 for util in vm_utilization)

            # Combine penalties
            fitness = load_balance_penalty + overload_penalty
            fitness_scores.append(fitness)

        return np.array(fitness_scores)


    def update_population(self, population, fitness_scores, tasks, vms, iteration):
        """
        Updates the population based on the GWO logic.

        Args:
            population (np.ndarray): Current population of wolves.
            fitness_scores (np.ndarray): Fitness values for the population.
            tasks (list): List of tasks.
            vms (list): List of VMs.
            iteration (int): Current iteration number.

        Returns:
            np.ndarray: Updated population.
        """
        a = self.a_max * (1 - iteration / self.max_iterations)

        # Identify alpha, beta, and delta wolves
        sorted_indices = np.argsort(fitness_scores)
        alpha, beta, delta = population[sorted_indices[0]], population[sorted_indices[1]], population[sorted_indices[2]]

        new_population = np.copy(population)
        for i, wolf in enumerate(population):
            for j in range(len(tasks)):
                r1, r2 = np.random.random(), np.random.random()
                A1, C1 = 2 * a * r1 - a, 2 * r2
                D_alpha = abs(C1 * alpha[j] - wolf[j])
                X1 = alpha[j] - A1 * D_alpha

                r1, r2 = np.random.random(), np.random.random()
                A2, C2 = 2 * a * r1 - a, 2 * r2
                D_beta = abs(C2 * beta[j] - wolf[j])
                X2 = beta[j] - A2 * D_beta

                r1, r2 = np.random.random(), np.random.random()
                A3, C3 = 2 * a * r1 - a, 2 * r2
                D_delta = abs(C3 * delta[j] - wolf[j])
                X3 = delta[j] - A3 * D_delta

                # Update wolf position
                new_population[i][j] = (X1 + X2 + X3) / 3

        return np.clip(new_population, 0, len(vms) - 1).astype(int)

    def optimize(self, tasks, vms):
        """
        Runs the GWO optimization.

        Args:
            tasks (list): List of tasks.
            vms (list): List of VMs.

        Returns:
            np.ndarray: Best allocation found.
        """
        population = self.initialize_population(tasks, vms)
        best_fitness = float('inf')
        best_allocation = None

        for iteration in range(self.max_iterations):
            fitness_scores = self.evaluate_fitness(population, tasks, vms)
            if min(fitness_scores) < best_fitness:
                best_fitness = min(fitness_scores)
                best_allocation = population[np.argmin(fitness_scores)]

            if best_fitness < self.convergence_threshold:
                break

            population = self.update_population(population, fitness_scores, tasks, vms, iteration)

        return best_allocation
