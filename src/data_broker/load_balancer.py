import time
import threading
import json
import os
import pandas as pd
from src.config.parser import ConfigParser
from src.data_broker.task_queue import TaskQueue
from src.data_broker.task_monitor import TaskMonitor
from src.cloud.task import Task
from src.cloud.pm import PM
from src.cloud.vm import VM
from src.algorithms.metaheuristic.pco import PlantCompetitionOptimization
from src.algorithms.metaheuristic.pso import ParticleSwarmOptimization
from src.algorithms.metaheuristic.gwo import GrayWolfOptimization

class LoadBalancer:
    """
    LoadBalancer class responsible for distributing tasks among available resources.
    """

    ENERGY_COEFFICIENT = 1.2  # Energy coefficient (adjust based on your system)

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
            "PSO": ParticleSwarmOptimization(algorithm_config["PSO"]),
            "GWO": GrayWolfOptimization(algorithm_config["GWO"]),
        }
        
        self.metrics = {
            "makespan": [],
            "sla_violations": [],
            "cpu_utilization": [],
            "execution_time": [],
            "tasks_executed": [],
            "energy_consumption": []  # New metric for energy consumption
        }
        self.start_time = None

    def collect_metrics(self, results):
        """
        Collect and store metrics from a single simulation run.
        """
        self.metrics["makespan"].append(results.get("makespan", 0))
        self.metrics["sla_violations"].append(results.get("sla_violation", 0))
        self.metrics["cpu_utilization"].append(results.get("cpu_utilization", 0))
        self.metrics["execution_time"].append(results.get("execution_time", 0))
        self.metrics["tasks_executed"].append(results.get("tasks_executed", 0))
        self.metrics["energy_consumption"].append(results.get("energy_consumption", 0))  # Collect energy consumption

    def calculate_metrics(self, tasks, vm_list, start_time, end_time):
        """
        Calculates metrics for the current load balancing execution.

        Args:
            tasks (list): List of tasks processed.
            vm_list (list): List of VM instances.
            start_time (float): Start time of the execution.
            end_time (float): End time of the execution.

        Returns:
            dict: Calculated metrics.
        """
        total_tasks = len(tasks)
        makespan = max(vm.calculate_makespan() for vm in vm_list)  # Max end time of tasks
        cpu_utilization = sum(vm.cpu_usage_percent() for vm in vm_list) / len(vm_list)  # Average CPU usage
        execution_time = end_time - start_time

        # Calculate energy consumption
        energy_consumption = cpu_utilization * self.ENERGY_COEFFICIENT

        return {
            "makespan": makespan,
            "sla_violation": 0,  # Placeholder if SLA violation is tracked
            "cpu_utilization": cpu_utilization,
            "execution_time": execution_time,
            "tasks_executed": total_tasks,
            "energy_consumption": energy_consumption
        }

    def run_task_monitor(self):
        """
        Starts the TaskMonitor GUI in a separate thread.
        """
        task_monitor = TaskMonitor(vms=self.vms, update_interval=25)  # Pass data queue
        task_monitor.run()

    def save_metrics(self, algorithm_name):
        """
        Save collected metrics to a CSV file.
        """
        os.makedirs(f"data/results/{algorithm_name}/", exist_ok=True)
        df = pd.DataFrame(self.metrics)
        filename = f"data/results/{algorithm_name}/metrics_{algorithm_name}.csv"
        df.to_csv(filename, index=False)
        print(f"Metrics saved to {filename}")

    def balance_load(self, algorithm_name):
        """
        Balances the load using the specified algorithm.

        Args:
            algorithm_name (str): Name of the algorithm to use for optimization.
        """
        if algorithm_name not in self.algorithms:
            raise ValueError(f"Algorithm '{algorithm_name}' not found.")
        
        conf = ConfigParser.get_config_dict()

        algorithm = self.algorithms[algorithm_name]

        # Process tasks from the task queue
        self.start_time = time.time()
        total_loop_time = 0
        loop_count = 0

        all_tasks = []  # Collect all tasks processed
        for file_name, tasks in self.task_queue.stream_work_load(self.algorithm_config[algorithm_name]["batch_size"]):
            loop_start_time = time.time()
            print(f"Processing tasks from file: {file_name}")
            all_tasks.extend(tasks)  # Add to the total task list

            # Run the optimization algorithm
            best_allocation = algorithm.optimize(tasks, self.vms)

            # Display task-to-VM allocation
            for task_cpu, vm_idx in zip(tasks, best_allocation):
                vm = self.vms[vm_idx]
                task = Task(task_cpu, execution_time=conf["task_queue"]["cpu_utilization_period"])
                allocated = vm.allocate_task(task)
                print(f"Task{task.task_id} {task_cpu} assigned to VM {vm.vm_id}", f"allocated {allocated}")

            loop_end_time = time.time()
            loop_time = loop_end_time - loop_start_time
            total_loop_time += loop_time
            loop_count += 1
            time.sleep(.09)  # Simulate processing delay

        # Calculate final metrics
        end_time = time.time()
        metrics = self.calculate_metrics(all_tasks, self.vms, self.start_time, end_time)
        self.collect_metrics(metrics)

        print(f"Load balancing completed using {algorithm_name}. Metrics: {metrics}")
