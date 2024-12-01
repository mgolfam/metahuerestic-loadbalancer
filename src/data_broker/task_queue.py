# src/data_broker/task_queue.py

import os

class TaskQueue:
    """
    Manages tasks by reading CPU utilization files from a specified directory.
    """

    def __init__(self, directory):
        """
        Initializes the task queue by loading tasks from the specified directory.

        Args:
            directory (str): Path to the directory containing asset files.
        """
        self.work_load = {}
        self.load_tasks(directory)

    def load_tasks(self, directory):
        """
        Reads all files in the given directory and loads tasks.

        Args:
            directory (str): Path to the directory containing asset files.
        """
        if not os.path.exists(directory) or not os.path.isdir(directory):
            raise FileNotFoundError(f"Directory '{directory}' not found or invalid.")

        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                self.read_file(file_name, file_path)

    def read_file(self, file_name, asset_file):
        """
        Reads a single asset file and adds its contents as a list to the tasks.

        Args:
            asset_file (str): Path to the asset file containing CPU utilizations.
        """
        file_tasks = []
        with open(asset_file, "r") as file:
            for line in file:
                try:
                    cpu_utilization = float(line.strip())
                    if cpu_utilization > 0:
                        file_tasks.append(cpu_utilization/100)
                except ValueError:
                    print(f"Invalid CPU utilization value in file '{asset_file}': {line.strip()}")
        if file_tasks:
            self.work_load[file_name] = file_tasks
    
    def stream_work_load(self, batch_size=None):
        """
        Streams the data from the work_load dictionary file by file in batches.

        Args:
            batch_size (int, optional): Number of rows to stream at a time. If None, streams all rows.

        Yields:
            tuple: A tuple containing the file name and a batch of normalized CPU utilizations.
        """
        for file_name, rows in self.work_load.items():
            if batch_size is None:
                yield file_name, rows
            else:
                for i in range(0, len(rows), batch_size):
                    yield file_name, rows[i:i + batch_size]

# Example usage
if __name__ == "__main__":
    # Assuming 'assets/dataset' is the directory containing asset files
    directory = "assets/dataset/list"

    task_queue = TaskQueue(directory)

    # print(task_queue.work_load)
    
    for file_name, rows in task_queue.stream_work_load(50):
        print(f"Streaming file: {file_name}")
        for row in rows:
            print(f"Normalized CPU Utilization: {row}")
