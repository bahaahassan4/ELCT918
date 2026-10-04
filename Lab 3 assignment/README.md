# Lab Assignment 3: Real-Time Handwritten Digit Recognition

**From a Trained CNN to a Webcam OCR Pipeline**

**ELCT918 – Selected Topics in AI Accelerators Hardware Design**
German University in Cairo (GUC), Faculty of Information Engineering and Technology

**Submitted by:** Shrouq Mohamed, BahaaElDin Hassan
**Submitted to:** MSc Eng. Nour ElShahawy

---

## Project Overview

A model that scores well on its test set is not yet a working system. A camera produces images with a different size, colour format, background, lighting and framing from anything the network saw during training. This project closes that gap: it takes the LeNet-5 network from Lab 2, retrains it on handwritten digits, and builds a preprocessing pipeline and a real-time application that recognises digits written on paper and held in front of a webcam.

| Part | What it does |
|---|---|
| **Task 1** | Retrains LeNet-5 on MNIST (grayscale, zero-padded from 28×28 to 32×32) with a fixed random seed |
| **Task 2** | `preprocess()` turns a photo or webcam crop of a handwritten digit into an MNIST-like 32×32 tensor |
| **Task 3** | `realtime_digit.py` runs the model on a live camera feed (or a video file) and shows the prediction, confidence and FPS |
| **Bonus 1** | LeNet-5 retrained on MADBase (AHDD1) to recognise Arabic-Indic digits (٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩) |
| **Bonus 2** | A single 20-class model that recognises both Western and Arabic-Indic digits, with a cross-system confusion analysis |

### Results

| Model | Classes | Test accuracy | Parameters | Time / epoch |
|---|---|---|---|---|
| LeNet-5 on MNIST (Task 1) | 10 | 98.98% | 61,706 | 40.77 s |
| LeNet-5 on MADBase (Bonus 1) | 10 | 98.44% | 61,706 | 51.90 s |
| LeNet-5 combined (Bonus 2) | 20 | 98.52% | 62,556 | 99.69 s |

All models were trained for 5 epochs with Adam (learning rate 1e-3) and batch size 32. Training times were measured on Google Colab.

### The preprocessing pipeline

MNIST digits are white on black, scaled to fit a 20×20 box with their aspect ratio preserved, and centred in a 28×28 image. `preprocess(roi)` reproduces this in five steps:

1. **Grayscale and blur:** convert the BGR camera image to grayscale and apply a Gaussian blur to reduce noise.
2. **Threshold and invert:** Otsu's method separates ink from paper; inversion makes the digit white on black.
3. **Crop:** find the largest contour and crop to its bounding box.
4. **Resize and centre:** scale the longer side to 20 pixels (aspect ratio kept), centre it in a 28×28 canvas, then pad to 32×32.
5. **Tensor:** scale to [0, 1], standardise with the training mean and standard deviation, and reshape to (1, 32, 32, 1).

---

## Repository Contents

| File | Description |
|---|---|
| `Task1_LeNet5_MNIST.ipynb` | Task 1: training notebook (MNIST) |
| `Lab3_bonus.ipynb` | Bonus: MADBase training and the combined 20-class model |
| `preprocess.py` | Task 2: preprocessing pipeline; run directly to produce the step-by-step figure |
| `realtime_digit.py` | Task 3: real-time webcam application |
| `combined_arabic_model/realtime_digit.py` | Real-time application for the 20-class model (labels Arabic digits as `ar0`–`ar9`) |
| `lenet5_mnist.keras` | Trained weights: MNIST model |
| `lenet5_MADBase.keras` | Trained weights: Arabic-Indic model |
| `lenet5_combined.keras` | Trained weights: combined 20-class model |
| `requirements.txt` | Python dependencies |

### Demo recordings

- Task 3 (Western digits 0–9): [link to recording](<add-link-here>)
- Bonus (Arabic-Indic digits): [link to recording](<add-link-here>)

---

## Installation

The real-time application must run **locally on your own computer**: Google Colab runs on a remote server and cannot access your camera. Training can be done in Colab (see [Retraining the models](#retraining-the-models)), but the trained weights are already included, so no training is needed to run the demo.

**Requirements:** Python 3.10–3.13 and a webcam (or a recorded video).

### 1. Clone the repository

```bash
git clone https://github.com/bahaahassan4/ELCT918.git
cd "ELCT918/Lab 3 assignment"
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

| Terminal | Activate with |
|---|---|
| Windows Command Prompt | `venv\Scripts\activate` |
| Windows PowerShell | `venv\Scripts\Activate.ps1` |
| macOS / Linux | `source venv/bin/activate` |

If PowerShell reports that running scripts is disabled, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then activate again.

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt` contains:

```
tensorflow==2.20.0
opencv-python
numpy
matplotlib
```

The TensorFlow version matches the one used for training in Colab, so the saved `.keras` files load correctly. On Windows, TensorFlow runs on the CPU, which is more than fast enough for LeNet-5 inference.

Check the installation:

```bash
python -c "import tensorflow as tf, cv2; print(tf.__version__, cv2.__version__)"
```

---

## Running the Scripts

Run all commands from the `Lab 3 assignment` folder with the virtual environment active.

### Task 2: Preprocessing figure (`preprocess.py`)

Processes a single photo of a handwritten digit, saves a figure of the five preprocessing steps, and prints the model's prediction.

1. Write a digit on white paper with a thick dark marker and take a photo.
2. Put the photo in this folder and set `IMAGE_PATH` near the bottom of `preprocess.py` to its file name.
3. Run:

```bash
python preprocess.py
```

The figure is shown on screen and saved as a PNG. Close the figure window to see the predicted digit and its confidence in the terminal.

### Task 3: Real-time recognition (`realtime_digit.py`)

```bash
python realtime_digit.py
```

Hold a digit written on white paper inside the box in the centre of the frame. Two windows open:

- **Real-time digit recognition:** the camera feed with the predicted digit, its confidence (softmax probability), the top-3 predictions and the FPS.
- **Model's view:** the 28×28 image the network receives, enlarged 10×.

The box colour shows the state: **green** for a confident prediction, **orange** ("?") when confidence is below the threshold, and **red** when no digit is detected.

Press **q** (with one of the windows selected) to quit.

#### Command-line options

| Option | Default | Description |
|---|---|---|
| `--source` | `0` | Camera index (`0`, `1`, `2`, …) or path to a video file |
| `--model` | `lenet5_mnist.keras` | Trained model to load |
| `--box` | `250` | Side length of the centre box, in pixels |
| `--threshold` | `0.70` | Confidence below which the prediction is shown as "?" |
| `--min-contrast` | `40` | Minimum brightness difference between ink and paper (0–255) |
| `--min-digit` | `0.15` | Minimum digit size, as a fraction of the box |
| `--save` | none | Save the annotated video to this file |

#### Using a phone as the camera

Install **DroidCam** or **Iriun Webcam** on your phone and the matching client on your laptop, and connect over USB (most stable) or Wi-Fi. The phone then appears as an ordinary camera; try indices `1` and `2` until you get the phone's image:

```bash
python realtime_digit.py --source 1
```

University Wi-Fi often blocks devices from talking to each other. Use USB, or connect the laptop to your phone's hotspot.

### Running on a video file instead of a live camera

If no live camera works, record a video of your handwritten digits with your phone, copy it into this folder, and pass its path to `--source`:

```bash
python realtime_digit.py --source my_digits.mp4
```

The same code handles both, because `cv2.VideoCapture` accepts a file path in place of a camera index. The application stops when the video ends.

To also save the annotated result:

```bash
python realtime_digit.py --source my_digits.mp4 --save annotated_output.mp4
```

### Bonus: Arabic-Indic digits

**MADBase model (10 Arabic-Indic classes):**

```bash
python realtime_digit.py --model lenet5_MADBase.keras
```

**Combined 20-class model (Western and Arabic-Indic):**

```bash
cd combined_arabic_model
python realtime_digit.py --model ../lenet5_combined.keras
```

Western digits are shown as `0`–`9` and Arabic-Indic digits as `ar0`–`ar9`. OpenCV's built-in fonts cannot draw Arabic characters, so the `ar` prefix is used instead.

The `--source` and `--save` options work the same way with both models, including running on a video file.

### Tips for good recognition

- Use a **thick dark marker** on **white paper**. Thin ballpoint strokes almost disappear when the digit is shrunk to 20 pixels.
- Write one digit at a time, large, and keep fingers and the paper's edges **outside** the box: the largest contour must be the digit.
- Use even lighting without strong shadows.
- If a prediction is wrong, look at the **Model's view** window first. It usually shows the cause: a stroke too thin, a digit broken into pieces, or the wrong object cropped. For thin strokes, enable the `cv2.dilate` line in `preprocess.py`.

---

## Retraining the Models

The notebooks are designed for **Google Colab** with a GPU runtime (**Runtime → Change runtime type → T4 GPU**).

### Task 1: MNIST

Open `Task1_LeNet5_MNIST.ipynb` in Colab and run all cells. MNIST downloads automatically through `tf.keras.datasets`. At the end, download the saved `.keras` file and place it in this folder.

### Bonus: MADBase and the combined model, using your own Kaggle token

The bonus notebook downloads the MADBase / AHDD1 dataset from Kaggle. **No Kaggle token is stored in this repository**; each user supplies their own.

**1. Create a Kaggle API token**

Sign in to [kaggle.com](https://www.kaggle.com), then go to your **profile picture → Settings → API** and create a new token. Copy it and keep it private.

**2. Add the token to Colab Secrets**

1. In Colab, click the **key icon** in the left sidebar.
2. Click **Add new secret**, name it `KAGGLE_API_TOKEN`, and paste your token as the value.
3. Turn on **Notebook access**.

Secrets are stored in your Google account, not in the notebook file, so the token never appears in the code or in GitHub.

**3. Run the notebook**

The notebook reads the token from Colab Secrets:

```python
import os
from google.colab import userdata

os.environ["KAGGLE_API_TOKEN"] = userdata.get("KAGGLE_API_TOKEN")
```

and then downloads the dataset:

```python
!kaggle datasets download -d mloey1/ahdd1 --unzip
```

**Running the download locally instead of in Colab:** set the token as an environment variable in your terminal session (it is not saved to any file), then download:

```powershell
# Windows PowerShell
$env:KAGGLE_API_TOKEN="your-token"
```

```bash
# macOS / Linux
export KAGGLE_API_TOKEN="your-token"
```

```bash
pip install kaggle
kaggle datasets download -d mloey1/ahdd1 --unzip
```

> **Never commit your Kaggle token to the repository.** If a token is ever exposed, expire it on Kaggle (Settings → API) and create a new one.

**Note on the MADBase CSV files:** each image is stored as a flattened row of 784 values, and reshaping it directly with `.reshape(28, 28)` gives rotated and mirrored digits. The notebook fixes this with a transpose (`.reshape(28, 28).T`, or `.transpose(0, 2, 1)` for a batch).

---

## Reproducibility

Training uses a fixed random seed. On a GPU, some operations are not fully deterministic because the order of floating-point additions in parallel threads can vary, so results may differ by a fraction of a percent between runs with the same seed.

---

## References

- Y. LeCun, L. Bottou, Y. Bengio and P. Haffner, "Gradient-Based Learning Applied to Document Recognition," *Proceedings of the IEEE*, 1998.
- MNIST database of handwritten digits.
- MADBase / AHDD1: Arabic Handwritten Digits Dataset, available on Kaggle.
