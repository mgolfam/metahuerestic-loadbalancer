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
        task_queue_dir = ConfigParser.get_config()["task_queue"]["directory"]
        self.task_queue = TaskQueue(task_queue_dir)
        self.load_balancer = LoadBalancer(self.task_queue, self.datacenter.pms)
    
    def start(self):
        pco_config = {"num_plants": 10, "iterations": 50}
        load_balancer.start(algorithm_name="PCO", algorithm_config=pco_config, batch_size=5)
