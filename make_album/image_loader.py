import os
import re


def load_images(folder):
    files = os.listdir(folder)
    images = []

    for f in files:
        if re.search(r'\.(png|jpg|jpeg|PNG|JPG|JPEG)$', f):
            images.append(os.path.join(folder, f))

    def sort_key(x):
        nums = re.findall(r'\d+', x)
        return int(nums[-1]) if nums else 9999999

    images.sort(key=sort_key)
    return images
