# utils/model_loader.py
import torch
from transformers import AutoImageProcessor, DetrForSegmentation

MODEL_ID = "cmarkea/detr-layout-detection"

processor = AutoImageProcessor.from_pretrained(MODEL_ID)
model = DetrForSegmentation.from_pretrained(MODEL_ID)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

__all__ = ["processor", "model", "device"]
