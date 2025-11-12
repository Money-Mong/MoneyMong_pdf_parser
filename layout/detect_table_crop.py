import os, torch
from datetime import datetime
from PIL import Image
from utils.detr_loader import processor, model, device


def detect_table_crop(page_img_path, report_id, page_number=1, threshold=0.4):
    image = Image.open(page_img_path).convert("RGB")
    W, H = image.size
    inputs = processor(images=image, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    results = processor.post_process_object_detection(
        outputs, threshold=threshold, target_sizes=[image.size[::-1]]
    )[0]

    table_layout_boxes = []
    crop_dir = os.path.join(os.getcwd(), "work_dir", "crops")
    os.makedirs(crop_dir, exist_ok=True)

    for i, (label, box) in enumerate(zip(results["labels"], results["boxes"])):
        # 라벨명 추출 및 정규화
        raw_label = model.config.id2label[label.item()].strip().lower()

        # Table만 저장
        if raw_label != "table":
            continue

        x0, y0, x1, y1 = map(int, box.tolist())

        # 3% 패딩 적용해서 crop
        pad_x = int(W * 0.03)
        pad_y = int(H * 0.03)
        x0 = max(0, x0 - pad_x)
        y0 = max(0, y0 - pad_y)
        x1 = min(W, x1 + pad_x)
        y1 = min(H, y1 + pad_y)

        # PDF 좌표 변환
        scale_x, scale_y = 595.0 / W, 842.0 / H
        pdf_y0, pdf_y1 = H - y1, H - y0
        pdf_bbox = [x0 * scale_x, pdf_y0 * scale_y, x1 * scale_x, pdf_y1 * scale_y]

        # ✅ Table 크롭 저장
        crop_path = os.path.join(crop_dir, f"{report_id}_b{i+1}_table.png")
        image.crop((x0, y0, x1, y1)).save(crop_path)

        table_layout_boxes.append({
            "document_id": report_id,
            "asset_type": "table",
            "page_number": page_number,
            "file_path": crop_path,
            "raw_data": None,
            "description": None,
            "extracted_text": None,
            "metadata": {"bbox_pdf": pdf_bbox, "bbox_image": [x0, y0, x1, y1]},
            "created_at": datetime.utcnow().isoformat()
        })
   
    return table_layout_boxes
