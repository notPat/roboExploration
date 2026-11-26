# Cooperative Multi-Robot Exploration

Bachelor's thesis in Computer Science at Leibniz University Hannover, March 2026.

Original thesis title: *Erkundung von unbekanntem Gelände durch kooperierende Roboter*

## Overview

This project investigates how multiple autonomous robots can cooperate to explore unknown environments and generate three-dimensional maps.

I developed a simulation in Unreal Engine 5 to implement and evaluate two exploration algorithms. The robots simulate LiDAR sensors using raycasts and periodically exchange collected data through a central communication node.

## Features

- Configurable number of robots, exploration time and exploration strategy
- Autonomous navigation using waypoints and behavior trees
- Simulated LiDAR sensors using raycasting
- Spatial partitioning and point cloud aggregation
- Synchronization of exploration data between robots during exploration
- 3D point cloud generation and visualization
- Export of simulation data in CSV and XYZ formats

## Exploration Algorithms

Two exploration approaches were developed and evaluated:

### Frontier-based Exploration

Robots select waypoints near sectors with a low number of scanned points, prioritizing areas that have not yet been sufficiently explored.

This approach is inspired by frontier-based exploration but uses sector density instead of explicitly identifying frontier cells.

### Greedy Nearest Waypoint Exploration

Robots select the nearest available waypoint while keeping track of previously visited waypoints. Once all eligible waypoints have been visited, the exploration cycle starts again.

## Data Processing and Analysis

Simulation data is collected, aggregated and exported for further analysis.

Python scripts were developed to process the recorded data and generate statistics and visualizations, including:

- Aggregation of scanned point counts across spatial sectors
- Top-down and individual Z-layer heatmaps with logarithmic scaling
- Exploration progress over time
- Individual robot contributions
- Calculation of scan statistics
- Comparison of exploration strategies

The scripts process CSV files, simulation metadata and, where required, PTS and XYZ point cloud files.

Pandas is used for data aggregation and transformation, NumPy for numerical processing and Matplotlib for visualization.

## Experiments and Results

The experiments were conducted in two different simulated environments:

- **Sewer:** A complex underground sewer system
- **TestTown:** An urban environment with buildings and open areas

Both exploration strategies were tested in each environment using configurations of 3, 5 and 8 robots, for 600 Seconds resulting in a total of 12 experimental runs.

Both algorithms produced comparable results in open environments. The frontier-based approach proved more suitable for complex terrain in these experiments, although both approaches showed limitations in such environments.

## Technologies

| Technology | Purpose |
|---|---|
| Unreal Engine 5.6.1 | Simulation environment |
| C++ | Implementation of simulation functionality |
| Blueprints | Visual scripting and robot behavior |
| LiDAR Point Cloud Plugin | Point cloud generation and visualization |
| Python | Experimental data analysis |
| Pandas | Data aggregation and transformation |
| NumPy | Numerical computations |
| Matplotlib | Data visualization |

## Analysis Scripts

The Python scripts are provided in the form originally used for the bachelor's thesis.

### Requirements

Python 3 and the following packages are required for heatmap generation:

```bash
pip install pandas numpy matplotlib
```

The statistics scripts use Python's standard library and require no additional packages.

### Heatmap Generation

The heatmap script reads `SectorDensityMap.csv` from the current working directory and generates a top-down heatmap and individual heatmaps for each Z-layer.

The resulting images are saved in the `heatmap_output` directory.

### Scan Statistics

To process an individual experimental run:

```bash
python scan_stats_generator_minimal.py --input PATH --output PATH
```

To process multiple experimental runs recursively:

```bash
python scan_stats_generator_recursive.py --input PATH
```

The scripts generate CSV files containing scan statistics, including sector counts, scanned points and scan rates.

The `explored_sectors_per_second` field is calculated using the recorded sector count divided by the simulation duration.

## Repository

This repository documents the simulation, experimental methodology and data analysis of the bachelor's thesis.

The complete Unreal Engine project is not included due to its size. The full experimental dataset is approximately 4 GB, and the complete raw point cloud data is not included.
Instead there is example data of two testruns, that can be viewed.
## Author

Patrick Bastek  
Leibniz University Hannover
