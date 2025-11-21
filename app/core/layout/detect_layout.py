# detect_layout.py
import json
import torch
from datetime import datetime
from PIL import Image
from app.core.layout.model_loader import get_detr_model

"""페이지 이미지에서 레이아웃(텍스트, 표, 이미지 등)을 감지 각 요소의 라벨, 박스 좌표 반환"""

def detect_layout(image: Image.Image, report_id, page_number=1, threshold=0.4):

    W, H = image.size
    processor, model, device = get_detr_model()

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
            "report_id": report_id,
            "page_number": page_number,               
            "element_type": tag,                      
            "element_order": idx + 1,                 
            "bbox": bbox_json,                        
            "content": None,                          
            "asset_id": None,                         
            "metadata": json.dumps({                  
                "image_size": [W, H]
            }),
            "created_at": datetime.utcnow().isoformat()
        })

    return layout_elements
