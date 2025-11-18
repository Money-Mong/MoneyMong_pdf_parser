# utils/file_loader.py
import boto3
import tempfile
from config.paths import S3_BUCKET, S3_RAW_PREFIX

s3 = boto3.client("s3")

def download_s3_pdf_to_temp(bucket, key):
    """S3 PDF → 임시파일 다운로드 후 로컬 경로 반환"""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        s3.download_fileobj(bucket, key, tmp)
        return tmp.name

