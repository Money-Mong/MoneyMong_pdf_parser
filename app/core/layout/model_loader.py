# app/core/layout/model_loader.py

import torch
from transformers import AutoImageProcessor, DetrForSegmentation

MODEL_ID = "cmarkea/detr-layout-detection"

_processor = None
_model = None
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def get_detr_model():
    global _model, _processor

    if _model is None or _processor is None:
        _processor = AutoImageProcessor.from_pretrained(MODEL_ID)
        _model = DetrForSegmentation.from_pretrained(MODEL_ID).to(_device)
        print("✅ DETR model loaded.")

    return _processor, _model, _device
