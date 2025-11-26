import pkg_resources
import os

def write_requirements():
    """プロジェクトルートに requirements.txt を生成"""

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    path = os.path.join(project_root, "requirements.txt")

    required = ["Pillow", "reportlab", "tqdm"]
    lines = []

    for pkg in required:
        try:
            ver = pkg_resources.get_distribution(pkg).version
            lines.append(f"{pkg}=={ver}")
        except:
            lines.append(f"{pkg}  # version not found")

    with open(path, "w") as f:
        f.write("\n".join(lines))

    print(f"requirements.txt を作成しました → {path}")


from io import BytesIO

def compress_image(img, quality):
    """
    Pillow Image → 圧縮JPEG(Memory buffer)
    quality: 1〜95
    """
    buf = BytesIO()
    img.save(buf, format="JPEG", quality=quality, optimize=True)
    buf.seek(0)
    return buf

