from src.config.parser import init_config
from src.simulation import simulate_loadbalancer

def main():
    simulate_loadbalancer()

if __name__ == "__main__":
    init_config()
    main()
    