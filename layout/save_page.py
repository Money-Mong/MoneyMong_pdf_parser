import os
from pdf2image import convert_from_path

def save_first_page(pdf_path, report_id):
    pages = convert_from_path(pdf_path, dpi=400, first_page=1, last_page=1)
    if not pages: raise RuntimeError("No pages rendered.")
    out_path = os.path.join("work_dir", "pages", f"{report_id}_p1.jpg")
    pages[0].save(out_path)
    return out_path
