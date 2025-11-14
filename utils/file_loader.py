# utils/file_loader.py
import os
import boto3
import tempfile

from config.paths import S3_BUCKET, S3_RAW_PREFIX

s3 = boto3.client("s3")

"""S3에서 PDF를 로컬 임시 파일로 다운로드하고 경로 반환"""
def download_s3_pdf_to_temp(bucket, key):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        s3.download_fileobj(bucket, key, tmp)
        return tmp.name

"""S3 : 임시파일로 다운로드해서 로컬 경로 리스트 반환"""
def get_local_pdf_files():
    pdf_paths = []

    response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=S3_RAW_PREFIX)
    contents = response.get("Contents", [])
    for obj in contents:
        key = obj["Key"]
        if not key.endswith(".pdf"):
            continue
        local_path = download_s3_pdf_to_temp(S3_BUCKET, key)
        pdf_paths.append((key, local_path))                                         # 원래 S3 key와 로컬 경로 함께 반환

    return pdf_paths
