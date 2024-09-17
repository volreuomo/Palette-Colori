import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


def ottieni_palette_da_immagine(image_path: str, num_colors: int = 5):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((100, 100))  # per performance
    img_array = np.array(img)
    img_array = img_array.reshape((-1, 3))

    # Applicla machine learning
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(img_array)
    colori = kmeans.cluster_centers_

    hex_colors = [rgb_a_hex(colore) for colore in colori]

    return hex_colors


def rgb_a_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
