# utils/file_loader.py
import os
import boto3

s3 = boto3.client("s3")

def download_s3_pdf_to_temp(bucket, key, tmp_dir='/tmp'):
    os.makedirs(tmp_dir, exist_ok=True)
    
    local_path = os.path.join(tmp_dir, os.path.basename(key))
    
    s3.download_file(bucket, key, local_path)

    return local_path

