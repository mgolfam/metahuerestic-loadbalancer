import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_metrics_from_dir(dir_path, algorithm_name):
    """Load all CSV files in a directory and label them with the algorithm name."""
    csv_files = [os.path.join(dir_path, file) for file in os.listdir(dir_path) if file.endswith('.csv')]
    dataframes = [pd.read_csv(file).assign(Algorithm=algorithm_name, Configuration=file.split('_conf')[1].split('.')[0]) for file in csv_files]
    return pd.concat(dataframes, ignore_index=True)

def load_all_metrics(base_dir):
    """Load metrics for all algorithms based on subdirectories."""
    all_data = []
    for algo in os.listdir(base_dir):
        algo_path = os.path.join(base_dir, algo)
        if os.path.isdir(algo_path):  # Check if it's a directory
            all_data.append(load_metrics_from_dir(algo_path, algo))
    return pd.concat(all_data, ignore_index=True)

def plot_metrics_for_configs(metrics_df, metrics_to_plot):
    """Create separate windows for each configuration."""
    configurations = metrics_df['Configuration'].unique()
    for config in configurations:
        config_data = metrics_df[metrics_df['Configuration'] == config]
        num_metrics = len(metrics_to_plot)
        cols = 2  # Number of columns in the grid
        rows = -(-num_metrics // cols)  # Ceiling division for rows
        fig, axes = plt.subplots(rows, cols, figsize=(12, 5 * rows), dpi=100)
        
        # Set a title for the entire window
        fig.suptitle(f'Metrics for Configuration {config}', fontsize=16, y=1.02)
        
        axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]
        
        for i, metric in enumerate(metrics_to_plot):
            ax = axes[i]
            config_data.groupby('Algorithm')[metric].mean().plot(kind='bar', ax=ax)
            ax.set_title(f'{metric}', fontsize=12)
            ax.set_ylabel(metric, fontsize=10)
            ax.set_xlabel('Algorithm', fontsize=10)
            ax.tick_params(axis='both', labelsize=10)
            ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Hide unused subplots
        for i in range(len(metrics_to_plot), len(axes)):
            fig.delaxes(axes[i])
        
        # Adjust spacing between rows and overall layout
        plt.subplots_adjust(hspace=0.5, wspace=0.6, top=0.9)
        plt.tight_layout(pad=5.0)
        plt.show()

# Define the base directory containing results
base_directory = 'data/results'

# Load all metrics
metrics = load_all_metrics(base_directory)

# Metrics to plot
metrics_to_compare = [
    'makespan',
    'sla_violation',
    'sla_violation_percent',
    'cpu_utilization',
    'execution_time',
    'energy_consumption'
]

# Plot the metrics for each configuration
plot_metrics_for_configs(metrics, metrics_to_compare)
