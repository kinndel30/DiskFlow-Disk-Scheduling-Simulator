# DiskFlow – Disk Scheduling Simulator

A Python-based Disk Scheduling Simulator with a graphical user interface (GUI) that demonstrates and compares three disk scheduling algorithms: FCFS, SSTF, and SCAN.

## Features

- Implements FCFS (First-Come, First-Served).
- Implements SSTF (Shortest Seek Time First).
- Implements SCAN (Elevator Algorithm).
- Accepts user-defined disk requests and initial head position.
- Supports disk range and scan direction configuration.
- Displays disk head movements and total head movement.
- Provides step-by-step computation and algorithm explanations.
- Allows users to compare algorithm results.
- Includes automated tests for algorithms, edge cases, and result formatting.

## Technologies Used

- Python
- Tkinter (GUI)
- Python Unittest (Testing)

## Project Structure

    DiskSchedulingSimulator/
    ├── algorithms/
    │   ├── __init__.py
    │   ├── fcfs.py
    │   ├── sstf.py
    │   └── scan.py
    ├── results/
    │   ├── __init__.py
    │   └── formatter.py
    ├── utils/
    │   ├── __init__.py
    │   └── validation.py
    ├── gui.py
    ├── main.py
    ├── requirements.txt
    ├── test_algorithms.py
    ├── test_edge_cases.py
    ├── test_formatter.py
    └── README.md

## Installation and Setup

1. Clone the repository:

       git clone https://github.com/kinndel30/DiskFlow-Disk-Scheduling-Simulator.git

2. Navigate to the project directory:

       cd DiskFlow-Disk-Scheduling-Simulator

3. Run the application:

       python main.py

## Running the Tests

To run all automated tests, execute:

    python -m unittest discover -v

## Disk Scheduling Algorithms

**FCFS (First-Come, First-Served)**

Processes disk requests in their arrival order.

**SSTF (Shortest Seek Time First)**

Selects the pending request closest to the current head position.

**SCAN (Elevator Algorithm)**

Moves the disk head in one direction, reaches the disk boundary, then reverses direction.

## Purpose

DiskFlow aims to provide an interactive way to understand disk scheduling algorithms, visualize disk head movements, and compare their performance based on total head movement.
