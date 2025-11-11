from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal

def extract_text(pdf_path, layout_boxes):
    def overlap(a, b):
        ax0, ay0, ax1, ay1 = a
        bx0, by0, bx1, by1 = b
        dx, dy = min(ax1, bx1) - max(ax0, bx0), min(ay1, by1) - max(ay0, by0)
        if dx <= 0 or dy <= 0:
            return 0.0
        inter = dx * dy
        a_area = (ax1 - ax0) * (ay1 - ay0)
        return inter / a_area

    text_blocks = []
    # 첫번째 페이지에 대해서만 텍스트 추출
    for p, page in enumerate(extract_pages(pdf_path)):
        if p > 0:
            break  
        for e in page:
            if isinstance(e, LTTextBoxHorizontal):
                # layout_boxes(표 영역 등)과 10% 이상 겹치지 않는 텍스트만 추출
                if all(overlap(e.bbox, lb['metadata']["bbox_pdf"]) < 0.1 for lb in layout_boxes):
                    text_blocks.append(e.get_text())

    return "\n".join(text_blocks)

