# manager.py
from src.config.parser import ConfigParser
from src.cloud.datacenter import Datacenter
from src.cloud.pm import PM
from src.cloud.vm import VM
from src.cloud.task import Task

from src.data_broker.task_queue import TaskQueue
from src.data_broker.load_balancer import LoadBalancer

class DataBrokerManager:
    def __init__(self, datacenter):
        self.datacenter = datacenter
        
        
        # Load TaskQueue
        task_queue_dir = ConfigParser.get_config_dict()["task_queue"]["directory"]
        self.task_queue = TaskQueue(task_queue_dir)
        
        conf = ConfigParser.get_config_dict()
        algorithm_config = conf["metaheuristics"]
        self.load_balancer = LoadBalancer(self.task_queue, self.datacenter.pms, algorithm_config)
    
    def start(self):
        # Run load balancing with metaheuristic algorithms from config
        for algorithm_name in ["PCO"]:
            self.load_balancer.balance_load(algorithm_name=algorithm_name)
