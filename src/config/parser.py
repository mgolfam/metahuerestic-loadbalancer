import json

class ConfigParser:
    """
    Utility class to parse and manage application configurations.
    """

    def __init__(self, config_file):
        """
        Initializes the ConfigParser.

        Args:
            config_file (str): Path to the JSON configuration file.
        """
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self):
        """
        Loads the configuration from the JSON file.

        Returns:
            dict: Parsed configuration data.
        """
        try:
            with open(self.config_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file '{self.config_file}' not found.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON configuration file: {e}")

    def get(self, key, default=None):
        """
        Retrieves a configuration value.

        Args:
            key (str): Dot-separated key path (e.g., "load_balancer.default_algorithm").
            default: Default value if the key does not exist.

        Returns:
            Any: Configuration value or the default value.
        """
        keys = key.split(".")
        value = self.config
        try:
            for k in keys:
                value = value[k]
            return value
        except KeyError:
            return default
        
    def as_dict(self):
        """
        Returns the entire configuration as a dictionary.
        """
        return self.config
    
    def get_config():
        # Load configuration
        return _config_instance
    
    def get_config_dict():
        # Load configuration
        return _config_instance.as_dict()
    
def init_config(config_file="config.json"):
    """
    Initializes and returns a singleton ConfigParser instance.

    This function ensures that the configuration is loaded only once.

    Args:
        config_file (str): Path to the JSON configuration file. Defaults to "config.json".

    Returns:
        ConfigParser: Singleton instance of ConfigParser with the loaded configuration.
    """
    global _config_instance
    if _config_instance is None:
        try:
            _config_instance = ConfigParser(config_file)
            print(f"Configuration initialized from {config_file}.")
        except (FileNotFoundError, ValueError) as e:
            print(f"Error initializing configuration: {e}")
            raise
    return _config_instance


_config_instance = ConfigParser("config.json")