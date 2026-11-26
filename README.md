# Cooperative Multi-Robot Exploration

Bachelor's thesis in Computer Science at Leibniz University Hannover, March 2026.

Original title: *Erkundung von unbekanntem Gelände durch kooperierende Roboter*

## Overview

This project investigates how multiple autonomous robots can cooperate to explore unknown environments and generate three-dimensional maps.

A simulation was developed in Unreal Engine 5 to implement and evaluate two exploration algorithms. The robots simulate LiDAR sensors using raycasts and share collected data through a central communication node.

## Features

- Configurable number of robots and exploration time
- Autonomous navigation and waypoint selection
- Simulated LiDAR sensors using raycasting
- Spatial partitioning and point cloud aggregation
- Synchronization of exploration data between robots at exploration time
- 3D point cloud visualization
- Export of simulation data in CSV and XYZ formats

## Exploration Algorithms

Two exploration approaches were developed and evaluated:

### Frontier-based Exploration

Robots select waypoints near sectors with a low density of scanned points, prioritizing areas that have not yet been sufficiently explored.

### Greedy Nearest Waypoint Exploration

Robots select the nearest available waypoint while keeping track of previously visited waypoints.

## Data Processing and Analysis

Simulation data is collected, aggregated and exported for further analysis.

Python scripts were used to process and visualize the recorded data, including:

- Number of scanned points per sector
- Exploration progress over time
- Individual robot contributions
- Comparison of exploration strategies

The experiments were conducted in two different environments using configurations of 3, 5 and 8 robots.

## Results

Both algorithms produced comparable results in open environments. The frontier-based approach proved more suitable for complex terrain, although both approaches showed limitations in such environments.

## Technologies

| Technology | Purpose |
|---|---|
| Unreal Engine 5.6.1 | Simulation environment |
| C++ | Implementation of simulation functionality |
| Blueprints | Visual scripting and robot behavior |
| LiDAR Point Cloud Plugin | Point cloud generation and visualization |
| Pandas | Data processing |
| NumPy | Numerical computations |
| Matplotlib | Data visualization |

## Repository

The complete Unreal Engine project is not included in this repository due to its size.

## Author

Patrick Bastek  
Leibniz University Hannover
