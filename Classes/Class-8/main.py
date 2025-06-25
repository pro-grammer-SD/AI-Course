import os
from shutil import rmtree
from pathlib import Path
import cv2
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Process

base_dir = Path(__file__).parent
image_path = base_dir / "samples" / "image.png"
output_dir = base_dir / "output"
image = cv2.imread(str(image_path))

def save_plot(img, title, file_name, cmap=None):
    plt.imshow(img, cmap=cmap)
    plt.title(title)
    plt.axis('off')
    plt.savefig(output_dir / file_name, bbox_inches='tight')
    plt.close()

def show_rgb():
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    save_plot(img, "RGB Image", "output_1.png")

def show_gray():
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    save_plot(img, "Grayscale Image", "output_2.png", cmap='gray')

def show_crop():
    img = cv2.cvtColor(image[80:100, 30:60], cv2.COLOR_BGR2RGB)
    save_plot(img, "Cropped Region", "output_3.png")

def show_rotate():
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, 45, 1.0)
    img = cv2.warpAffine(image, M, (w, h))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    save_plot(img, "Rotated Image", "output_4.png")

def show_bright():
    brighter = cv2.add(image, np.ones(image.shape, dtype="uint8") * 50)
    img = cv2.cvtColor(brighter, cv2.COLOR_BGR2RGB)
    save_plot(img, "Brighter Image", "output_5.png")

if __name__ == '__main__':
    rmtree(output_dir, ignore_errors=True)
    output_dir.mkdir()

    tasks = [show_rgb, show_gray, show_crop, show_rotate, show_bright]
    processes = [Process(target=task) for task in tasks]

    for p in processes:
        p.start()

    for p in processes:
        p.join()
