# TODO: S3 경로로 변경

import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.getcwd()
PDF_FOLDER = os.path.join(BASE_DIR, "test_pdf") #input_pdfs 
WORK_DIR = os.path.join(BASE_DIR, "work_dir")
JSON_DIR = os.path.join(WORK_DIR, "json")
CROP_DIR = os.path.join(WORK_DIR, "crops")
IMG_DIR = os.path.join(WORK_DIR, "pages")
for path in [PDF_FOLDER, WORK_DIR, JSON_DIR, CROP_DIR, IMG_DIR]:
    os.makedirs(path, exist_ok=True)
