import os
from PIL import Image
from tqdm import tqdm


def generate_pdfs(folder, quality, output_name=None, custom_filename=None, progress_callback=None):

    # 画像読み込み
    files = sorted([
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ])

    if not files:
        raise ValueError("画像が見つかりません。")

    # 出力フォルダ名
    base_name = output_name if output_name else os.path.basename(folder.rstrip("/"))
    outdir = os.path.join(os.path.dirname(folder), base_name)
    os.makedirs(outdir, exist_ok=True)

    # 品質設定
    if quality == "high":
        dpi = 300
    elif quality == "standard":
        dpi = 200
    else:
        dpi = 150

    # 進捗用カウンタ
    total_steps = len(files) * 2   # A4 + 原寸の2種類を作っているため
    step = 0

    # ==============================
    #  A4版 PDF
    # ==============================
    a4_pdf_path = os.path.join(outdir, f"{custom_filename or 'album'}_A4.pdf")
    images_a4 = []

    for f in tqdm(files, desc="A4版 作成中"):
        img = Image.open(f).convert("RGB")
        img = img.resize((2480, 3508))   # A4 300dpi
        images_a4.append(img)

        step += 1
        if progress_callback:
            progress_callback(step / total_steps)

    images_a4[0].save(a4_pdf_path, save_all=True, append_images=images_a4[1:])

    # ==============================
    #  原寸版（見開き）
    # ==============================
    raw_pdf_path = os.path.join(outdir, f"{custom_filename or 'album'}_raw.pdf")
    images_raw = []

    for f in tqdm(files, desc="原寸版 見開き作成中"):
        img = Image.open(f).convert("RGB")
        images_raw.append(img)

        step += 1
        if progress_callback:
            progress_callback(step / total_steps)

    images_raw[0].save(raw_pdf_path, save_all=True, append_images=images_raw[1:])

    return outdir
