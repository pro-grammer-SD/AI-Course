from PIL import Image

img = Image.open("image.png")
img = img.convert("L")

img.show()
