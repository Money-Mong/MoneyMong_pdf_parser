# detect_layout.py
import json
import torch
from datetime import datetime
from PIL import Image
from utils.detr_loader import processor, model, device

def detect_layout(page_img_path, report_id, page_number=1, threshold=0.4):
    """
    페이지 이미지에서 레이아웃(텍스트, 표, 이미지 등)을 감지
    각 요소의 라벨, 박스 좌표 반환
    """
    image = Image.open(page_img_path).convert("RGB")
    W, H = image.size

    inputs = processor(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)

    results = processor.post_process_object_detection(
        outputs, threshold=threshold, target_sizes=[image.size[::-1]]
    )[0]

    layout_elements = []
    for idx, (label, box) in enumerate(zip(results["labels"], results["boxes"])):
        tag = model.config.id2label[label.item()].strip().lower()
        x1, y1, x2, y2 = map(float, box.tolist())
        bbox_json = {"x1": x1, "y1": y1, "x2": x2, "y2": y2}

        layout_elements.append({
            # "id": str(uuid.uuid4()),                  # PK
            "document_id": report_id,               # FK → documents.id
            "page_number": page_number,               # 페이지 번호
            "element_type": tag,                        # 요소 타입
            "element_order": idx + 1,                 # 페이지 내 순서
            "bbox": bbox_json,                        # 박스 좌표
            "content": None,                          # 텍스트 추출 시 채워짐
            "asset_id": None,                         # table/image 등은 후처리 시 채워짐
            "metadata": json.dumps({                  # confidence 등 부가정보
                "image_size": [W, H]
            }),
            "created_at": datetime.utcnow().isoformat()
        })

    return layout_elements
