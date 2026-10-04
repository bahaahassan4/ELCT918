"""
preprocess.py - ELCT918 Lab 3, Task 2
Preprocessing pipeline: turns a photo/crop of a handwritten digit into a
32x32 tensor matching the exact distribution LeNet-5 was trained on in Task 1.
wanna run it on my local machine
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

# must match EXACTLY what was used to train lenet5_mnist.keras in Task 1
MNIST_MEAN = 0.1307
MNIST_STD = 0.3081


def preprocess(roi):
    """
    roi: a BGR color image (as OpenCV reads it) containing a handwritten
         digit on paper - either a full photo or a cropped camera region.

    Returns:
        tensor: (1, 32, 32, 1) float32 array ready for model.predict(), or
                None if no digit was found in the image.
        steps:  dict of intermediate images, for the Task 2 deliverable figure.
    """
    steps = {}

    # 1. Grayscale + blur (reduce camera sensor noise)
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    steps['1_gray'] = gray

    # 2. Threshold + invert -> white digit on black background, like MNIST
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    # if pen strokes are thin and get lost, thicken them:
    # thresh = cv2.dilate(thresh, np.ones((3, 3), np.uint8), iterations=1)
    steps['2_thresh'] = thresh

    # 3. Crop to the digit's bounding box
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        steps['3_cropped'] = thresh  # nothing found, show the blank threshold
        return None, steps
    largest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest)
    digit = thresh[y:y + h, x:x + w]
    steps['3_cropped'] = digit

    # 4. Resize (preserve aspect ratio, larger side -> 20px),
    #    center in 28x28, then pad to 32x32 (matches Task 1's padding)
    h, w = digit.shape
    if h >= w:
        new_h = 20
        new_w = max(1, round(w * 20 / h))
    else:
        new_w = 20
        new_h = max(1, round(h * 20 / w))
    resized = cv2.resize(digit, (new_w, new_h), interpolation=cv2.INTER_AREA)

    canvas28 = np.zeros((28, 28), dtype=np.uint8)
    y_off = (28 - new_h) // 2
    x_off = (28 - new_w) // 2
    canvas28[y_off:y_off + new_h, x_off:x_off + new_w] = resized

    canvas32 = cv2.copyMakeBorder(canvas28, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=0)
    steps['4_centered'] = canvas32

    # 5. Convert to tensor: scale to [0,1], standardize with the SAME mean/std as training
    tensor = canvas32.astype('float32') / 255.0
    tensor = (tensor - MNIST_MEAN) / MNIST_STD
    tensor = tensor.reshape(1, 32, 32, 1)
    steps['5_final_input'] = canvas32  # keep uint8 version just for display

    return tensor, steps


def show_pipeline_figure(steps, save_path='task2_pipeline_figure6.png'):
    """Deliverable: a figure showing the output of each step for one digit."""
    fig, axes = plt.subplots(1, len(steps), figsize=(3 * len(steps), 3))
    if len(steps) == 1:
        axes = [axes]
    for ax, (name, img) in zip(axes, steps.items()):
        ax.imshow(img, cmap='gray')
        ax.set_title(name)
        ax.axis('off')
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.show()
    print(f"Saved pipeline figure to {save_path}")


if __name__ == "__main__":
    # ---- quick standalone test / Task 2 deliverable generation ----
    # replace with a photo of a handwritten digit on paper (phone photo or
    # a single webcam frame saved to disk)
    IMAGE_PATH = "my_digit_photo6.jpg"

    roi = cv2.imread(IMAGE_PATH)
    if roi is None:
        raise FileNotFoundError(f"Could not read {IMAGE_PATH} - check the path.")

    tensor, steps = preprocess(roi)
    show_pipeline_figure(steps)

    if tensor is not None:
        # sanity-check prediction using the Task 1 model
        model = tf.keras.models.load_model("lenet5_mnist.keras")
        probs = model.predict(tensor, verbose=0)[0]
        pred = int(np.argmax(probs))
        confidence = float(probs[pred])
        print(f"Predicted digit: {pred}  (confidence: {confidence:.2%})")
    else:
        print("No digit detected in the image - check lighting/contrast.")