import json
from src.config.parser import ConfigParser
from src.data_broker.task_queue import TaskQueue
from src.cloud.pm import PM
from src.cloud.vm import VM
from src.algorithms.metaheuristic.pco import PlantCompetitionOptimization
from src.algorithms.metaheuristic.pso import ParticleSwarmOptimization
from src.algorithms.metaheuristic.gwo import GreyWolfOptimization

class LoadBalancer:
    """
    LoadBalancer class responsible for distributing tasks among available resources.
    """

    def __init__(self, task_queue, pm_list):
        """
        Initializes the LoadBalancer.

        Args:
            task_queue (TaskQueue): An instance of TaskQueue to provide tasks.
            pm_list (list): List of PM objects to balance load across.
        """
        self.task_queue = task_queue
        self.pm_list = pm_list

    def configure_algorithm(self, algorithm_name, **kwargs):
        """
        Configures and initializes a metaheuristic algorithm.

        Args:
            algorithm_name (str): Name of the algorithm ('PCO', 'PSO', 'GWO').
            **kwargs: Additional parameters for the algorithm.

        Returns:
            object: Configured algorithm instance.
        """
        if algorithm_name == "PCO":
            return PlantCompetitionOptimization(**kwargs)
        elif algorithm_name == "PSO":
            return ParticleSwarmOptimization(**kwargs)
        elif algorithm_name == "GWO":
            return GreyWolfOptimization(**kwargs)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")

    def balance_load(self, algorithm, batch_size=None):
        """
        Balances the load by distributing tasks using the specified algorithm.

        Args:
            algorithm (object): Metaheuristic algorithm instance for optimization.
            batch_size (int, optional): Number of tasks to process at a time. If None, process all tasks.
        """
        for file_name, tasks in self.task_queue.stream_work_load(batch_size=batch_size):
            print(f"Processing tasks from file: {file_name}")
            for task in tasks:
                # Use the algorithm to find the best PM and VM
                best_allocation = algorithm.optimize(self.pm_list, task)
                if best_allocation:
                    pm, vm = best_allocation
                    if vm.allocate_task(cpu_demand=task, memory_demand=1):
                        print(f"Task with CPU demand {task} assigned to VM on PM {pm.pm_id}.")
                    else:
                        print(f"Task with CPU demand {task} could not be allocated.")
                else:
                    print(f"No suitable PM or VM found for task {task}.")

    def start(self, algorithm_name, algorithm_config):
        """
        Starts the load balancing process with the specified algorithm.

        Args:
            algorithm_name (str): Name of the algorithm to use ('PCO', 'PSO', 'GWO').
            algorithm_config (dict): Configuration parameters for the algorithm, including batch_size.
        """
        print(f"Starting load balancing with algorithm: {algorithm_name}")
        batch_size = algorithm_config.pop("batch_size", None)
        algorithm = self.configure_algorithm(algorithm_name, **algorithm_config)
        self.balance_load(algorithm, batch_size=batch_size)

