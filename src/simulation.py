# simulation.py
from src.config.parser import ConfigParser
from src.cloud.datacenter import Datacenter
from src.data_broker.manager import DataBrokerManager

def init_datacenter():
    # dc = Datacenter(5, 20, 2.8*1024, 64, 5)
    config = ConfigParser.get_config()
    dc = Datacenter(config.get("datacenter"))
    Datacenter.visualize_datacenter(dc)
    return dc
    
def init_data_broker(datacenter):
    data_broker = DataBrokerManager(datacenter)
    data_broker.start()

def simulate_loadbalancer():
    datacenter = init_datacenter()
    init_data_broker(datacenter=datacenter)