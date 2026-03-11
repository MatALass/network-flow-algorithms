# Network Flow Algorithms

Python project implementing and benchmarking classical network flow algorithms, including Ford-Fulkerson, Push-Relabel, and Minimum Cost Flow, with test cases, trace outputs, plotting utilities, and a Tkinter GUI.

## Project Overview

This repository explores core graph optimization problems through practical Python implementations of network flow algorithms. It provides:

- algorithm implementations for maximum flow and minimum cost flow problems
- reproducible test cases
- benchmark scripts for runtime comparison
- plotting utilities for execution-time analysis
- a desktop GUI for interactive execution

The project is designed as both an educational optimization project and a software engineering exercise around algorithm implementation, benchmarking, and visualization.

## Features

- Ford-Fulkerson implementation for maximum flow
- Push-Relabel implementation for maximum flow
- Minimum Cost Flow implementation
- CLI-style execution entry points
- Tkinter GUI for interactive use
- benchmark generation on random graphs
- plotting of runtime behavior across graph sizes
- trace file support for algorithm execution analysis

## Tech Stack

- Python
- Tkinter
- Matplotlib

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/MatALass/network-flow-algorithms.git
cd network-flow-algorithms 
```

### 2. Create and activate a virtual environment
python -m venv .venv

Windows:
```bash
.venv\Scripts\activate
```
macOS / Linux:
```bash
source .venv/bin/activate
```
### 3. Install dependencies

Using pyproject.toml:
```bash
pip install -e .
```

Or with requirements:
```bash
pip install -r requirements.txt
```
Usage

Run the CLI entry point
```bash
python scripts/run_cli.py
```
Launch the GUI
```bash
python scripts/run_gui.py
```
Run benchmarks
```bash
python scripts/benchmark.py
```
Plot benchmark results
```bash
python scripts/plot_results.py
```