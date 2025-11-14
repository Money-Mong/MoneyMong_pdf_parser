import boto3
import os, io, torch
from PIL import Image
from datetime import datetime
from utils.detr_loader import processor, model, device
from config.paths import (S3_BUCKET, S3_CROP_PREFIX, CROP_DIR)


s3 = boto3.client("s3")


def detect_table_crop(image: Image.Image, report_id, page_number=1, threshold=0.4):
    # 이미지 로드
    W, H = image.size

    # DETR 입력 준비
    inputs = processor(images=image, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    results = processor.post_process_object_detection(
        outputs, threshold=threshold, target_sizes=[image.size[::-1]]
    )[0]

    table_layout_boxes = []

    for i, (label, box) in enumerate(zip(results["labels"], results["boxes"])):
        raw_label = model.config.id2label[label.item()].strip().lower()

        # Table만 크롭
        if raw_label != "table":
            continue

        x0, y0, x1, y1 = map(int, box.tolist())

        # 패딩 적용
        pad_x = int(W * 0.03)
        pad_y = int(H * 0.03)
        x0 = max(0, x0 - pad_x)
        y0 = max(0, y0 - pad_y)
        x1 = min(W, x1 + pad_x)
        y1 = min(H, y1 + pad_y)

        # PDF 좌표 변환
        scale_x = 595.0 / W
        scale_y = 842.0 / H
        pdf_y0 = H - y1
        pdf_y1 = H - y0
        pdf_bbox = [x0 * scale_x, pdf_y0 * scale_y, x1 * scale_x, pdf_y1 * scale_y]

        filename = f"{report_id}_b{i+1}_table.png"


        # S3 저장
        s3_key = f"{S3_CROP_PREFIX}{filename}"

        # 이미지 메모리 저장 후 업로드
        buffer = io.BytesIO()
        image.crop((x0, y0, x1, y1)).save(buffer, format="PNG")
        buffer.seek(0)

        s3.upload_fileobj(buffer, S3_BUCKET, s3_key)

        crop_path = f"s3://{S3_BUCKET}/{s3_key}"

        # 저장된 테이블 box 정보 추가
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
