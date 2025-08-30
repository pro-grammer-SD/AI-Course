import argparse
import pytesseract
from PIL import Image, ImageFilter, ImageOps

def extract_text(path, pre_processor="thresh"):
    image = Image.open(path).convert("L")

    if pre_processor == "thresh":
        image = ImageOps.invert(ImageOps.autocontrast(image)).point(lambda x: 0 if x < 128 else 255, "1")
    elif pre_processor == "blur":
        image = image.filter(ImageFilter.MedianFilter(size=3))
    
    return pytesseract.image_to_string(image)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", default="image.png", help="📂 path to the image file")
    ap.add_argument("-p", "--pre_processor", default="thresh", choices=["thresh", "blur", "none"], help="📊 preprocessor usage")
    args = ap.parse_args()

    print(extract_text(args.image, args.pre_processor))
    