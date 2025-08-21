from fetch import fetch_ngrok_url, get_image

img = get_image("A cute cat wearing sunglasses", fetch_ngrok_url())
img.show()
