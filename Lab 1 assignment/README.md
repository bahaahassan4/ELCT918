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

The implementation cost of each neural network is evaluated using two different cost metrics.

## 1. Parameter Count Cost (Simple Proxy)

The first cost metric uses the total number of trainable parameters as a simple estimation of the hardware implementation cost:

```python
Total Parameters = sum(p.numel() for p in model.parameters())   
````
This metric represents the network size and the required memory storage for the model weights.

## 2. Hardware-Aware Cost Model

The second cost metric follows the cost model introduced in the reference paper.

The cost is calculated as:

$$ Cost = (\#Weights \times Weight\ Unit\ Cost) + (\#Multiplications \times Multiplication\ Unit\ Cost) $$

where:

- **#Weights** represents the total number of weights in all fully connected layers.
- **#Multiplications** represents the number of multiplication operations required during inference.
- **Weight Unit Cost** represents the normalized cost of accessing weights from memory.
- **Multiplication Unit Cost** represents the normalized computation cost.

The normalized values used are:

- Weight Unit Cost = 139
- Multiplication Unit Cost = 1

The multiplication cost is normalized to 1 based on the energy cost of a multiply-accumulate operation, while the weight access cost is set to 139 because memory access consumes significantly more energy compared to computation.

Therefore, the hardware-aware cost is calculated as:

Hardware Cost = (Number of Weights × 139) + (Number of Multiplications × 1)

Both cost metrics are applied consistently across all explored architectures and are used to analyze the trade-off between implementation cost and classification accuracy.

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

* Neural network cost (number of parameters/Hardware-Aware Cost)
* Accuracy drop

The plot can be found here:

```
pareto_front.png
pareto_front_hardwareawarecost.png
```

Example:
### For No. of parameters 
![Pareto Front](pareto_front.png)
### For Hardware-aware cost model
![pareto front hardware-aware cost](pareto_front_hardwareawarecost.png)

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
