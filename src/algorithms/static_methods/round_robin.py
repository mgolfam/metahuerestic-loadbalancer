# round_robin.py

class RoundRobinAllocator:
    """
    Implements a Round Robin scheduling algorithm for allocating tasks or VMs.
    """

    def __init__(self, resources):
        """
        Initialize the allocator with a list of resources.

        Args:
            resources (list): List of resources (e.g., PMs or VMs).
        """
        self.resources = resources
        self.index = 0

    def allocate(self, item):
        """
        Allocates an item (e.g., a task or VM) to the next available resource in a round-robin fashion.

        Args:
            item: The item to allocate.

        Returns:
            bool: True if allocation is successful, False otherwise.
        """
        if not self.resources:
            raise ValueError("No resources available for allocation.")

        for _ in range(len(self.resources)):
            resource = self.resources[self.index]
            self.index = (self.index + 1) % len(self.resources)

            if resource.add_vm(item):  # Assumes `add_vm` is defined in the resource class
                return True

        return False  # If no resource could allocate the item

# Example usage:
if __name__ == "__main__":
    from src.cloud.vm import VM
    from src.cloud.pm import PM

    # Create PMs
    pm1 = PM(cpu_core=8, cpu_speed=2000, memory=32)
    pm2 = PM(cpu_core=16, cpu_speed=2500, memory=64)

    # Initialize the Round Robin Allocator
    allocator = RoundRobinAllocator(resources=[pm1, pm2])

    # Create VMs
    vms = [VM(cpu_core=2, cpu_speed=2000, memory=8) for _ in range(5)]

    # Allocate VMs
    for vm in vms:
        success = allocator.allocate(vm)
        if success:
            print(f"VM allocated successfully.")
        else:
            print(f"Failed to allocate VM.")

    # Show free resources
    print(f"PM1 Free Resources: {pm1.show_free_resources()}")
    print(f"PM2 Free Resources: {pm2.show_free_resources()}")
