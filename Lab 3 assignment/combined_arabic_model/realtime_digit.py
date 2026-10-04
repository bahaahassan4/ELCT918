"""
realtime_digit.py - ELCT918 Lab 3, Task 3
Real-time handwritten digit recognition with LeNet-5 and a webcam.

Hold a digit written on white paper inside the green box.
Press 'q' to quit.

Usage:
    python realtime_digit.py                      # default camera (index 0)
    python realtime_digit.py --source 1           # another camera (e.g. phone via DroidCam/Iriun)
    python realtime_digit.py --source demo.mp4    # a recorded video file instead of a camera
    python realtime_digit.py --save output.mp4    # also save the annotated video

Requires preprocess.py (Task 2) and lenet5_mnist.keras (Task 1) in the same folder.
"""

import argparse
import time

import cv2
import numpy as np
import tensorflow as tf

from preprocess import preprocess   # Task 2 pipeline - the SAME code used for the figure


# ---------------------------------------------------------------------------
# Settings (can be overridden from the command line)
# ---------------------------------------------------------------------------
parser = argparse.ArgumentParser(description="Real-time handwritten digit recognition")
parser.add_argument("--source", default="0",
                    help="camera index (0, 1, 2, ...) or path to a video file")
parser.add_argument("--model", default="lenet5_combined.keras", help="trained model file")
parser.add_argument("--box", type=int, default=250, help="side of the centre box in pixels")
parser.add_argument("--threshold", type=float, default=0.70,
                    help="below this confidence the prediction is shown as '?'")
parser.add_argument("--min-digit", type=float, default=0.15,
                    help="ignore contours smaller than this fraction of the box (noise)")
parser.add_argument("--min-contrast", type=float, default=40,
                    help="minimum brightness difference between ink and paper (0-255)")
parser.add_argument("--save", default=None, help="optional path to save the annotated video")
args = parser.parse_args()

GREEN = (0, 200, 0)
ORANGE = (0, 165, 255)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = cv2.FONT_HERSHEY_SIMPLEX


def put_label(img, text, org, scale=0.8, color=WHITE, thickness=2):
    """Text with a dark outline so it stays readable on any background."""
    cv2.putText(img, text, org, FONT, scale, BLACK, thickness + 3, cv2.LINE_AA)
    cv2.putText(img, text, org, FONT, scale, color, thickness, cv2.LINE_AA)


# ---------------------------------------------------------------------------
# 1. Load the model (trained in Task 1 - no training happens here)
# ---------------------------------------------------------------------------
print("Loading model:", args.model)
model = tf.keras.models.load_model(args.model)

# One warm-up call so the first real frame is not slowed down by graph building
model(np.zeros((1, 32, 32, 1), dtype="float32"), training=False)


# ---------------------------------------------------------------------------
# 2. Open the camera or video file
# ---------------------------------------------------------------------------
source = int(args.source) if args.source.isdigit() else args.source
cap = cv2.VideoCapture(source)
if not cap.isOpened():
    raise SystemExit(f"Could not open source {args.source!r}. "
                     "Try --source 1 or --source 2, or check the video path.")
is_video_file = not isinstance(source, int)

ok, frame = cap.read()
if not ok:
    raise SystemExit("Could not read a frame from the source.")
frame_h, frame_w = frame.shape[:2]
box = min(args.box, frame_h, frame_w)
print(f"Frame size: {frame_w}x{frame_h} | box: {box}x{box} | press 'q' to quit")

writer = None
if args.save:
    fps_out = cap.get(cv2.CAP_PROP_FPS) or 20
    writer = cv2.VideoWriter(args.save, cv2.VideoWriter_fourcc(*"mp4v"),
                             fps_out, (frame_w, frame_h))

# Centre box coordinates
x1 = (frame_w - box) // 2
y1 = (frame_h - box) // 2
x2, y2 = x1 + box, y1 + box

MODEL_VIEW_SIZE = 280      # the 28x28 input enlarged 10x
fps = 0.0
prev_time = time.perf_counter()


# ---------------------------------------------------------------------------
# 3. Main loop: crop -> preprocess -> predict -> display
# ---------------------------------------------------------------------------
while True:
    if frame is None:
        ok, frame = cap.read()
        if not ok:
            print("End of video." if is_video_file else "Camera stopped sending frames.")
            break

    display = frame.copy()

    # Crop the centre box and run the Task 2 pipeline on it
    roi = frame[y1:y2, x1:x2]
    tensor, steps = preprocess(roi)

    # Decide whether the box really contains a digit, so an empty box shows "No digit".
    # On blank paper, Otsu still splits the image in two - but it splits camera noise,
    # so the "ink" is barely darker than the "paper" and covers a large area.
    if tensor is not None:
        gray, thresh = steps["1_gray"], steps["2_thresh"]
        ink, paper = gray[thresh > 0], gray[thresh == 0]
        contrast = float(paper.mean() - ink.mean()) if ink.size and paper.size else 0.0
        ink_fraction = float((thresh > 0).mean())
        crop_h, crop_w = steps["3_cropped"].shape[:2]
        if (contrast < args.min_contrast                     # no real ink, just noise
                or ink_fraction > 0.40                       # mostly "ink": a shadow, hand, or noise
                or max(crop_h, crop_w) < args.min_digit * box):  # only a tiny speck
            tensor = None

    # Model's view: the 28x28 image inside the 32x32 input, enlarged
    if tensor is not None:
        view28 = steps["4_centered"][2:30, 2:30]
    else:
        view28 = np.zeros((28, 28), dtype=np.uint8)
    model_view = cv2.resize(view28, (MODEL_VIEW_SIZE, MODEL_VIEW_SIZE),
                            interpolation=cv2.INTER_NEAREST)
    model_view = cv2.cvtColor(model_view, cv2.COLOR_GRAY2BGR)

    # Predict
    if tensor is not None:
        probs = model(tensor, training=False).numpy()[0]   # faster than predict() for 1 image
        digit = int(np.argmax(probs))
        confidence = float(probs[digit])
        top3 = np.argsort(probs)[::-1][:3]
        digit_combined = f"ar{int(digit) - 10}" if int(digit) > 9 else digit
        if confidence >= args.threshold:
            label, color = f"Digit: {digit_combined}", GREEN
        else:
            label, color = f"Digit: ? (best {digit_combined})", ORANGE
        #label_combined = f"ar{int(label) - 10}" if int(label) > 9 else label
        put_label(display, label, (x1, y1 - 45), scale=1.0, color=color)
        put_label(display, f"Confidence: {confidence * 100:.1f}%", (x1, y1 - 12), color=color)
        put_label(display, "Top 3: " + "  ".join(f"{d}:{probs[d] * 100:.0f}%" for d in top3),
                  (x1, y2 + 30), scale=0.6)
        put_label(model_view, str(digit_combined), (10, 40), scale=1.2, color=color)
    else:
        color = RED
        put_label(display, "No digit", (x1, y1 - 12), scale=1.0, color=RED)

    # FPS (smoothed so the number does not flicker)
    now = time.perf_counter()
    instant_fps = 1.0 / max(now - prev_time, 1e-6)
    prev_time = now
    fps = instant_fps if fps == 0 else 0.9 * fps + 0.1 * instant_fps
    put_label(display, f"FPS: {fps:.1f}", (10, 30), scale=0.8)
    put_label(display, "Press 'q' to quit", (10, frame_h - 15), scale=0.6)

    # Centre box (colour shows the state: green / orange / red)
    cv2.rectangle(display, (x1, y1), (x2, y2), color, 2)

    cv2.imshow("Real-time digit recognition", display)
    cv2.imshow("Model's view (28x28 input, enlarged)", model_view)
    if writer is not None:
        writer.write(display)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    frame = None   # read a new frame on the next iteration


# ---------------------------------------------------------------------------
# 4. Clean up
# ---------------------------------------------------------------------------
cap.release()
if writer is not None:
    writer.release()
    print("Saved annotated video to", args.save)
cv2.destroyAllWindows()