import os
from dotenv import load_dotenv
import boto3

load_dotenv()

# 환경 변수
S3_BUCKET = os.getenv("S3_BUCKET")
S3_RAW_PREFIX = os.getenv("S3_RAW_PREFIX", "raw-documents/")
S3_CROP_PREFIX = os.getenv("S3_CROP_PREFIX", "processed-documents/crops/")
S3_PAGE_IMG_PREFIX = os.getenv("S3_PAGE_IMG_PREFIX", "processed-documents/page-img/")
S3_JSON_PREFIX = os.getenv("S3_JSON_PREFIX", "processed-documents/json/")

# S3 전용 경로 설정
PDF_FOLDER = f"s3://{S3_BUCKET}/{S3_RAW_PREFIX}"
CROP_DIR = f"s3://{S3_BUCKET}/{S3_CROP_PREFIX}"
IMG_DIR = f"s3://{S3_BUCKET}/{S3_PAGE_IMG_PREFIX}"
JSON_DIR = f"s3://{S3_BUCKET}/{S3_JSON_PREFIX}"

s3 = boto3.client("s3")