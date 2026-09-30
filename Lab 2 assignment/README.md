# Lab 2: Comparative Study of Classical CNN Architectures

**ELCT918 – Selected Topics in AI Accelerators Hardware Design**
German University in Cairo (GUC)

**Prepared by:** Shrouq Mohamed Khalil, Bahaa ElDin Hassan Mohamed
**Course Instructor:** Dr. Eman Azab | **Teaching Assistant:** MSc. Eng. Nour ElShahawy

---

## Overview

This lab implements three classical convolutional neural networks from scratch (no pretrained weights), adapts them to the 32×32 input size of CIFAR, and compares them on architecture, model capacity, accuracy, and overfitting behaviour:

| Architecture | Paper |
|---|---|
| **LeNet-5** | LeCun, Bottou, Bengio & Haffner, *Gradient-Based Learning Applied to Document Recognition*, 1998 |
| **AlexNet** | Krizhevsky, Sutskever & Hinton, *ImageNet Classification with Deep Convolutional Neural Networks*, 2012 |
| **VGG16** | Simonyan & Zisserman, *Very Deep Convolutional Networks for Large-Scale Image Recognition*, 2014 |

Each architecture is trained and evaluated on both **CIFAR-10** (10 classes) and **CIFAR-100** (100 classes). LeNet-5 is implemented in two variants, giving **8 trained models** in total.

## Repository Contents

| File | Description |
|---|---|
| `Lab2.ipynb` | Google Colab notebook with all model definitions, training runs, results, and plots |
| `ELCT918_Lab2_Report.docx` | Full lab report: architectures, adaptations, results, and discussion |
| `README.md` | This file |

## Framework

All models are implemented in **TensorFlow / Keras**:

- **Sequential API:** LeNet-5 (full C3), AlexNet, VGG16
- **Functional API:** LeNet-5 (Table I partial C3), which needs per-branch connections the Sequential API cannot express

Using a single framework keeps layer implementations, default weight initialisation, and training mechanics identical across all models.

## Adaptations for 32×32 CIFAR Input

### LeNet-5
- Input depth changed from 1 (grayscale) to 3 (RGB); only C1's filter depth changes (156 → 456 parameters).
- Original Euclidean RBF output layer replaced with **Dense + Softmax**.
- Scaled tanh activation and trainable subsampling replaced with **ReLU** and plain **AveragePooling2D**, consistent with the other two networks.
- **Two variants:**
  - **Full C3:** every C3 filter sees all 6 S2 maps (2,416 C3 parameters).
  - **Table I C3:** the paper's partial-connectivity scheme, built with `tf.gather` + per-branch `Conv2D` + `Concatenate`, reproducing the paper's **1,516** C3 parameters exactly.

### AlexNet
- First convolution kept at 11×11 / stride 4 with `same` padding, which reduces the 32×32 input to 8×8 immediately.
- Local Response Normalization (LRN) omitted.
- The original two-GPU split (grouped Conv2, Conv4, Conv5) replaced with full connectivity.
- Dropout (0.5) kept on FC6 and FC7.
- Output layer sized to 10 or 100 classes.

### VGG16
- The 13 convolutional layers (3×3, `same` padding) are kept.
- **Pool4 and Pool5 removed**, since five 2×2 pooling stages would shrink a 32×32 input to 1×1; the feature map is 4×4×512 before the classifier.
- Classifier kept as FC 4096 → FC 4096 → output with dropout.

## Architecture Summary

| Model | Weight layers | Params (CIFAR-10) | Params (CIFAR-100) |
|---|---|---|---|
| LeNet-5 (full C3) | 5 | 62,006 | 69,656 |
| LeNet-5 (Table I C3) | 5 | 61,106 | 68,756 |
| AlexNet | 8 | 21,622,154 | 21,990,884 |
| VGG16 | 16 | 65,095,498 | 65,464,228 |

## Training Setup

Settings are fixed across all architectures for each dataset, so differences in results reflect architecture rather than training configuration.

| Setting | CIFAR-10 | CIFAR-100 |
|---|---|---|
| Optimizer | Adam | Adam |
| Learning rate | 1e-4 | 1e-5 |
| Epochs | 10 | 30 |
| Batch size | 32 | 32 |
| Loss | Sparse categorical cross-entropy | Sparse categorical cross-entropy |
| Preprocessing | Pixel values scaled to [0, 1] | Pixel values scaled to [0, 1] |
| Pretrained weights | None (trained from scratch) | None (trained from scratch) |

The official 10,000-image test split is used for evaluation, and the validation curves are computed on this split.

**Why the learning rate differs:** With Adam's default rate (1e-3), VGG16 stalled at a loss plateau of about ln(number of classes). A lower rate was needed for VGG16 to train, especially on CIFAR-100, and the same rate was then applied to all models on that dataset.

## Results

**Acc. Drop** is defined as 100% − Top-1 accuracy.

| Model | Dataset | Top-1 Acc. | Top-5 Acc. | Test Loss | Acc. Drop | Time / Epoch* |
|---|---|---|---|---|---|---|
| LeNet-5 (full C3) | CIFAR-10 | 51.16% | – | 1.3637 | 48.84% | ~6 s |
| LeNet-5 (Table I C3) | CIFAR-10 | 51.22% | – | 1.3690 | 48.78% | ~8 s |
| AlexNet | CIFAR-10 | 63.61% | – | 1.2227 | 36.39% | ~15 s |
| VGG16 | CIFAR-10 | **77.69%** | – | **0.8493** | **22.31%** | ~95 s |
| LeNet-5 (full C3) | CIFAR-100 | 11.96% | 32.05% | 3.8792 | 88.04% | ~6 s |
| LeNet-5 (Table I C3) | CIFAR-100 | 12.33% | 32.07% | 3.8674 | 87.67% | ~9 s |
| AlexNet | CIFAR-100 | 21.96% | 50.12% | **3.1709** | 78.04% | ~16 s |
| VGG16 | CIFAR-100 | **26.87%** | **55.27%** | 3.4965 | **73.13%** | ~98 s |

\* Typical epoch time on Google Colab, excluding the first epoch (which includes graph compilation). Top-5 accuracy was tracked for the CIFAR-100 runs only.

## Key Findings

- **Depth and capacity drive accuracy.** Accuracy rises from LeNet-5 to AlexNet to VGG16 on both datasets, and the accuracy drop shrinks with depth: 88.0% → 78.0% → 73.1% on CIFAR-100.
- **LeNet-5 underfits.** Its training and validation curves nearly overlap on both datasets. With about 62K parameters, it lacks the capacity to learn natural images.
- **Partial connectivity costs nothing.** LeNet-5's Table I C3 matches the full version (51.22% vs 51.16%) with 900 fewer parameters, supporting why modern networks dropped hand-designed connection tables.
- **AlexNet overfits on CIFAR-10 but not CIFAR-100.** On CIFAR-10, training accuracy reaches about 81% while validation accuracy plateaus near 63–64%. On CIFAR-100 (30 epochs, lower learning rate), the curves still track each other at epoch 30.
- **VGG16 overfits on both datasets.** On CIFAR-10, validation loss is lowest at epoch 6 and rises afterwards. On CIFAR-100, validation loss bottoms out at epoch 21 (2.94) and rises to 3.50, while training accuracy (52.6%) is nearly double validation accuracy (26.9%).
- **Higher accuracy does not always mean lower loss.** VGG16 beats AlexNet on CIFAR-100 in accuracy but has a higher test loss (3.50 vs 3.17). The overfit model makes overconfident wrong predictions.
- **CIFAR-100 is much harder.** Only about 500 training images per class (versus 5,000 in CIFAR-10) cause large accuracy drops for every architecture.
- **Computational cost scales with depth.** VGG16 takes about 15× longer per epoch than LeNet-5, and most of its 65M parameters (about 50M) sit in the fully-connected layers.

## How to Run

1. Open `Lab2.ipynb` in [Google Colab](https://colab.research.google.com/).
2. Select a GPU runtime: **Runtime → Change runtime type → GPU**.
3. Run the cells in order. Each cell trains one model on one dataset, then prints its test metrics and plots its accuracy and loss curves.

CIFAR-10 and CIFAR-100 are downloaded automatically through `tf.keras.datasets`, so no manual data setup is needed.

**Requirements** (preinstalled on Colab): Python 3, TensorFlow 2.x, Matplotlib.
