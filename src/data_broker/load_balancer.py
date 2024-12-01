import time
import threading
import json
from src.config.parser import ConfigParser
from src.data_broker.task_queue import TaskQueue
from src.data_broker.task_monitor import TaskMonitor
from src.cloud.task import Task
from src.cloud.pm import PM
from src.cloud.vm import VM
from src.algorithms.metaheuristic.pco import PlantCompetitionOptimization
# from src.algorithms.metaheuristic.pso import ParticleSwarmOptimization
# from src.algorithms.metaheuristic.gwo import GreyWolfOptimization

class LoadBalancer:
    """
    LoadBalancer class responsible for distributing tasks among available resources.
    """

    def __init__(self, task_queue, pm_list, algorithm_config):
        """
        Initializes the LoadBalancer.

        Args:
            task_queue (TaskQueue): An instance of TaskQueue to provide tasks.
            pm_list (list): List of PM objects to balance load across.
        """
        self.task_queue = task_queue
        self.pm_list = pm_list
        
        self.vms = []
        for pm in self.pm_list:
            self.vms.extend(pm.vms)  # Append VMs from the current PM
            
        # Initialize and start TaskMonitor in a separate thread
        self.task_monitor_thread = threading.Thread(target=self.run_task_monitor)
        self.task_monitor_thread.daemon = True  # Ensure it exits when the main program exits
        self.task_monitor_thread.start()
            
        self.algorithm_config = algorithm_config
        self.algorithms = {
            "PCO": PlantCompetitionOptimization(algorithm_config["PCO"]),
            # Add other algorithms here (e.g., PSO, GWO)
        }
        
    def run_task_monitor(self):
        """
        Starts the TaskMonitor GUI in a separate thread.
        """
        task_monitor = TaskMonitor(vms=self.vms, update_interval=300)  # Pass data queue
        task_monitor.run()

    def balance_load(self, algorithm_name):
        """
        Balances the load using the specified algorithm.

        Args:
            algorithm_name (str): Name of the algorithm to use for optimization.
        """
        if algorithm_name not in self.algorithms:
            raise ValueError(f"Algorithm '{algorithm_name}' not found.")

        algorithm = self.algorithms[algorithm_name]

        # Process tasks from the task queue
        for file_name, tasks in self.task_queue.stream_work_load(self.algorithm_config[algorithm_name]["batch_size"]):
            print(f"Processing tasks from file: {file_name}")

            # Run the optimization algorithm
            best_allocation = algorithm.optimize(tasks, self.vms)

            # Display task-to-VM allocation
            for task, vm_idx in zip(tasks, best_allocation):
                allocated = self.vms[vm_idx].allocate_task(Task(task, execution_time=5))
                print(f"Task {task} assigned to VM {vm_idx}", f"allocated {1}".format(allocated))

            # Optionally, update VM capacities based on assigned tasks
            # for task, vm_idx in zip(tasks, best_allocation):
                # self.vms[vm_idx] -= task  # Reduce VM capacity by the task's CPU requirement
                
            # Simulate a delay for task processing
            time.sleep(.1)


