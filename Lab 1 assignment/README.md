# ELCT918 Lab 1 Assignment  
## Multi-Objective Design Space Exploration of Neural Network Hyperparameters

This project is developed as part of **ELCT918 — Selected Topics in AI Accelerators Hardware Design** at the **German University in Cairo (GUC)**.

The objective of this assignment is to explore the trade-off between neural network implementation cost and classification accuracy by performing a **Multi-Objective Design Space Exploration (DSE)** over different fully connected neural network architectures.

The project uses a parameterizable neural network generator, trains different architectures on the **MNIST handwritten digit dataset**, evaluates their performance, and identifies the **Pareto-optimal configurations**.

---

# Project Overview

The project consists of two main parts:

## Task 1 — Parameterizable Neural Network Generator

A reusable fully connected neural network generator was implemented using **PyTorch**.

Instead of manually creating separate models for different architectures, a single parameterized model is generated dynamically depending on:

- Number of hidden layers (`n`)
- Number of nodes in each hidden layer (`m_array`)

The generated architecture follows:

```

Input Layer (784 neurons)
|
Hidden Layers
|
Output Layer (10 neurons)

```

where:

- 784 represents the flattened 28×28 MNIST image pixels.
- 10 represents the ten MNIST digit classes.

The model supports different depths and widths without modifying the network definition.

---

# Task 1 Training Setup

The neural networks are trained and evaluated using the MNIST dataset.

## Dataset

- Training samples: 60,000 images
- Testing samples: 10,000 images
- Image size: 28×28 grayscale pixels

## Training Configuration

| Parameter | Value |
|---|---|
| Framework | PyTorch |
| Loss Function | Cross-Entropy Loss |
| Optimizer | Adam |
| Learning Rate | 0.001 |
| Batch Size | 64 |
| Epochs | 10 |

---

# Task 1 Results

Several architectures were generated to verify that the network generator can successfully create and train different neural networks.

| Hidden Layers | Nodes per Layer | Parameters | Test Accuracy |
|---|---|---|---|
| 2 | [64,64] | 55,050 | 96.82% |
| 1 | [128] | 101,770 | 97.73% |
| 3 | [64,64,64] | 59,210 | 97.10% |
| 3 | [128,128,128] | 134,794 | 97.55% |

---

# Task 2 — Design Space Exploration

The second part performs a Design Space Exploration over different neural network configurations.

The explored parameters are:

## Number of Hidden Layers

```

n = 1 → 5

```

## Layer Widths

The node widths are selected from:

```

[10, 20, 40, 80, 160, 200]

````

Different architectures are generated, including:

- Uniform-width networks
- Increasing-width (funnel) networks
- Deep and shallow architectures

A total of **30 unique configurations** were trained and evaluated.

---

# Cost Model

The implementation cost of each network is measured using the total number of trainable parameters:

```python
Total Parameters = sum(p.numel() for p in model.parameters())
````

Each architecture is evaluated based on two objectives:

1. Minimize parameter count (hardware cost)
2. Minimize accuracy drop

where:

```
Accuracy Drop = 100 - Test Accuracy
```

---

# Pareto Front Analysis

A configuration is considered Pareto-optimal if no other configuration provides:

* Lower or equal cost
* Lower or equal accuracy drop

while being strictly better in at least one objective.

The Pareto-front computation is implemented using a dominance check over all explored configurations.

The final exploration produced **13 Pareto-optimal configurations**.

---

# Results Visualization

The project generates a Pareto-front plot showing the relationship between:

* Neural network cost (number of parameters)
* Accuracy drop

The plot can be found here:

```
pareto_front.png
```

Example:

![Pareto Front](pareto_front.png)

---

# Technologies Used

* Python 3
* PyTorch
* Torchvision
* NumPy
* Matplotlib
* Jupyter Notebook

---

# Installation

Clone the repository:

```bash
git clone https://github.com/bahaahassan4/ELCT918.git
```

Navigate to the assignment folder:

```bash
cd ELCT918/Lab\ 1\ assignment
```

Install the required dependencies:

```bash
pip install torch torchvision numpy matplotlib jupyter
```

---

# How to Run

1. Start Jupyter Notebook:

```bash
jupyter notebook
```

2. Open the project notebook.

3. Run the cells sequentially.

The notebook will:

* Load the MNIST dataset
* Generate neural network architectures
* Train each configuration
* Evaluate accuracy
* Calculate parameter count
* Compute the Pareto-optimal front
* Generate the Pareto-front visualization

---

# Project Structure

```
Lab 1 assignment/
│
├── README.md
│
├── <notebook_name>.ipynb
│
└── pareto_front.png
```

---

# Authors

**Shrouq Mohamed**
**BahaaElDin Hassan**

German University in Cairo
Faculty of Information Engineering and Technology

---

# Course Information

**Course:** ELCT918
**Course Title:** Selected Topics in AI Accelerators Hardware Design

**Lab Assignment:** 1
**Topic:** Multi-Objective Design Space Exploration of Neural Network Hyperparameters
