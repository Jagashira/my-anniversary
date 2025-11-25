from PIL import Image


def fit_to_a4(img_path, target_w, target_h):
    img = Image.open(img_path)
    w, h = img.size
    scale = min(target_w / w, target_h / h)
    return img, w * scale, h * scale


def get_original_size(img_path):
    img = Image.open(img_path)
    return img, img.size[0], img.size[1]
