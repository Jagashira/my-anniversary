from reportlab.lib.pagesizes import A4, landscape
from layout import fit_to_a4, get_original_size
from tqdm import tqdm


from reportlab.lib.pagesizes import A4, landscape
from layout import fit_to_a4, get_original_size
from tqdm import tqdm


def export_pdf_a4(pdf, images):
    """A4に1ページ1枚で写真をそのまま貼るPDF"""

    a4_w, a4_h = A4

    for i, img in enumerate(tqdm(images, desc="A4版 作成中")):
        pdf.setPageSize(A4)

        resized, w, h = fit_to_a4(img, a4_w, a4_h)

        # A4 中央に配置
        x = (a4_w - w) / 2
        y = (a4_h - h) / 2

        pdf.drawInlineImage(resized, x, y, w, h)
        pdf.showPage()




# ===============================
#  原寸PDF（縮小なし）
# ===============================
def export_pdf_original(pdf, images):

    cover_img, w, h = get_original_size(images[0])
    pdf.setPageSize((w, h))
    pdf.drawInlineImage(cover_img, 0, 0, w, h)
    pdf.showPage()

    for i in tqdm(range(1, len(images), 2), desc="原寸版 見開き作成中"):
        left_img, lw, lh = get_original_size(images[i])

        if i + 1 < len(images):
            right_img, rw, rh = get_original_size(images[i + 1])
        else:
            right_img, rw, rh = None, lw, lh

        spread_w = lw + rw
        spread_h = max(lh, rh)

        pdf.setPageSize((spread_w, spread_h))

        pdf.drawInlineImage(left_img, 0, 0, lw, lh)

        if right_img:
            pdf.drawInlineImage(right_img, lw, 0, rw, rh)

        pdf.showPage()
