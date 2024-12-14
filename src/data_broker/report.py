import matplotlib.pyplot as plt

class Report:
    """
    Class for generating and displaying comparison graphs for metaheuristic algorithms.
    """

    def __init__(self, results):
        """
        Initialize the Report class with results data.

        Args:
            results (dict): Dictionary containing results data for algorithms.
                            Example format:
                            {
                                "PSO": {"makespan": 100, "response_time": 50, "energy": 10},
                                "GWO": {"makespan": 120, "response_time": 45, "energy": 8}
                            }
        """
        self.results = results

    def generate_all_charts(self):
        """
        Generate all comparison charts (bar, line, pie, grouped bar) in a single window.
        """
        metrics = list(next(iter(self.results.values())).keys())
        algorithms = list(self.results.keys())

        fig, axs = plt.subplots(2, 2, figsize=(15, 10))

        # Bar chart for each metric
        for i, metric in enumerate(metrics):
            ax = axs[i // 2, i % 2]
            values = [self.results[algo][metric] for algo in algorithms]
            ax.bar(algorithms, values, color=['blue', 'orange', 'green', 'red'])
            ax.set_title(f"Comparison of {metric.replace('_', ' ').capitalize()}")
            ax.set_xlabel("Algorithms")
            ax.set_ylabel(metric.replace('_', ' ').capitalize())

        plt.tight_layout()
        plt.show()

    def generate_bar_chart(self, metric, title="Comparison Chart"):
        """
        Generate a bar chart for the specified metric.

        Args:
            metric (str): The metric to plot (e.g., 'makespan', 'response_time').
            title (str): The title of the chart.
        """
        algorithms = list(self.results.keys())
        values = [self.results[algo][metric] for algo in algorithms]

        plt.figure(figsize=(8, 6))
        plt.bar(algorithms, values, color=['blue', 'orange', 'green', 'red'])
        plt.title(title)
        plt.xlabel("Algorithms")
        plt.ylabel(metric.replace("_", " ").capitalize())
        plt.show()

    def generate_line_chart(self, metric, title="Performance Over Iterations"):
        """
        Generate a line chart for the specified metric.

        Args:
            metric (str): The metric to plot (e.g., 'makespan', 'response_time').
            title (str): The title of the chart.
        """
        plt.figure(figsize=(10, 6))

        for algo, data in self.results.items():
            if isinstance(data[metric], list):
                plt.plot(range(len(data[metric])), data[metric], label=algo)
            else:
                plt.plot([data[metric]], label=algo)

        plt.title(title)
        plt.xlabel("Iterations")
        plt.ylabel(metric.replace("_", " ").capitalize())
        plt.legend()
        plt.show()

    def generate_pie_chart(self, metric, title="Metric Distribution"):
        """
        Generate a pie chart for the specified metric.

        Args:
            metric (str): The metric to plot (e.g., 'energy').
            title (str): The title of the chart.
        """
        algorithms = list(self.results.keys())
        values = [self.results[algo][metric] for algo in algorithms]

        plt.figure(figsize=(8, 6))
        plt.pie(values, labels=algorithms, autopct='%1.1f%%', startangle=140)
        plt.title(title)
        plt.show()

    def generate_all_metrics_bar_chart(self, title="Algorithm Comparison Across Metrics"):
        """
        Generate a grouped bar chart for all metrics across algorithms.

        Args:
            title (str): The title of the chart.
        """
        metrics = list(next(iter(self.results.values())).keys())
        algorithms = list(self.results.keys())

        x = range(len(metrics))
        width = 0.2  # Width of each bar

        plt.figure(figsize=(12, 8))

        for i, algo in enumerate(algorithms):
            values = [self.results[algo][metric] for metric in metrics]
            plt.bar([pos + i * width for pos in x], values, width, label=algo)

        plt.title(title)
        plt.xlabel("Metrics")
        plt.ylabel("Values")
        plt.xticks([pos + width for pos in x], [metric.replace("_", " ").capitalize() for metric in metrics])
        plt.legend()
        plt.show()

# Example Usage
if __name__ == "__main__":
    # Mock results for demonstration
    mock_results = {
        "PSO": {"makespan": 100, "response_time": 50, "energy": 10, "resource_utilization": 80},
        "GWO": {"makespan": 120, "response_time": 45, "energy": 8, "resource_utilization": 85},
        "GA": {"makespan": 110, "response_time": 48, "energy": 9, "resource_utilization": 83}
    }

    report = Report(mock_results)
    report.generate_all_charts()
