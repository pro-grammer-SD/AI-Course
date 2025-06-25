from PIL import Image, ImageFilter, ImageEnhance

def resize_mr_tralalelo(img_path: str, scale: int) -> Image.Image:
    img = Image.open(img_path)
    (width, height) = (img.width * scale, img.height * scale)
    return img.resize((width, height), Image.Resampling.LANCZOS)

def improve_quality(img: Image.Image) -> Image.Image:
    img = img.filter(ImageFilter.DETAIL)
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2.5)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.4)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.3)
    return img

resized_img = resize_mr_tralalelo("image.png", 20)
better_resized_img = improve_quality(resized_img)
better_resized_img.save("mod_image.png")
better_resized_img.show()
