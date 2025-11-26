import sys
import os
from reportlab.pdfgen import canvas
from image_loader import load_images
from exporter import export_pdf_a4, export_pdf_original
from utils import write_requirements
import argparse


def main():

    folder = sys.argv[1]
    
    if not os.path.isdir(folder):
        print("フォルダが存在しません:", folder)
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("folder")
    parser.add_argument("--quality", default="high",
                        choices=["high", "standard", "light"])
    parser.add_argument("--output-name", default=None,
                    help="出力フォルダ名（未指定なら画像フォルダ名を使用）")
    args = parser.parse_args()

    quality_map = {
        "high": 90,
        "standard": 70,
        "light": 45
    }
    jpeg_quality = quality_map[args.quality]

    images = load_images(args.folder)

    if len(images) == 0:
        print("画像が見つかりません。png/jpg を入れてください。")
        sys.exit(1)

    # 出力先 dist/<folder>/
    if args.output_name:
        output_name = args.output_name
    else:
        output_name = os.path.basename(args.folder.rstrip('/'))

    outdir = os.path.join("dist", output_name)
    os.makedirs(outdir, exist_ok=True)

    # ---------- A4版 PDF ----------
    a4_pdf_path = f"{outdir}/album_A4.pdf"
    pdf_a4 = canvas.Canvas(a4_pdf_path)
    export_pdf_a4(pdf_a4, images,jpeg_quality)
    pdf_a4.save()

    # ---------- 原寸版 PDF ----------
    orig_pdf_path = f"{outdir}/album_original.pdf"
    pdf_orig = canvas.Canvas(orig_pdf_path)
    export_pdf_original(pdf_orig, images,jpeg_quality)
    pdf_orig.save()

    # ---------- requirements.txt の自動生成 ----------
    req_path = f"requirements.txt"
    write_requirements()

    print("=== PDF生成完了 ===")
    print(f"A4版: {a4_pdf_path}")
    print(f"原寸版: {orig_pdf_path}")
    print(f"requirements.txt: {req_path}")


if __name__ == "__main__":
    main()
