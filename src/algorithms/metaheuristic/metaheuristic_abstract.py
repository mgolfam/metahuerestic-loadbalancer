from abc import ABC, abstractmethod


class Metaheuristic(ABC):
    """
    Abstract base class for metaheuristic algorithms.
    """

    def __init__(self, config):
        """
        Initializes the metaheuristic algorithm with its configuration.

        Args:
            config (dict): Algorithm-specific configuration.
        """
        self.config = config

    @abstractmethod
    def initialize_population(self, tasks, vms):
        """
        Initializes the population for the optimization algorithm.

        Args:
            tasks (list): List of CPU utilization tasks.
            vms (list): List of VMs with their free CPU capacities.
        """
        pass

    @abstractmethod
    def evaluate_fitness(self, population, tasks, vms):
        """
        Evaluates the fitness of the population.

        Args:
            population (list): List of candidate solutions.
            tasks (list): List of CPU utilization tasks.
            vms (list): List of VMs with their free CPU capacities.
        """
        pass

    @abstractmethod
    def update_population(self, population, fitness_scores):
        """
        Updates the population based on fitness scores.

        Args:
            population (list): List of candidate solutions.
            fitness_scores (list): Fitness scores of the population.
        """
        pass

    def optimize(self, tasks, vms):
        """
        Runs the optimization process.

        Args:
            tasks (list): List of CPU utilization tasks.
            vms (list): List of VMs with their free CPU capacities.

        Returns:
            list: Optimized task-to-VM mapping.
        """
        population = self.initialize_population(tasks, vms)
        for _ in range(self.config.get("iterations", 50)):
            fitness_scores = self.evaluate_fitness(population, tasks, vms)
            self.update_population(population, fitness_scores)

        # Return the best solution
        best_solution = max(population, key=lambda p: self.evaluate_fitness([p], tasks, vms)[0])
        return best_solution
