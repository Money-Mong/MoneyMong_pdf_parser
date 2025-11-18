# save_page.py
import io
import boto3
from pdf2image import convert_from_path
from PIL import Image
from config.paths import S3_BUCKET, S3_PAGE_IMG_PREFIX

s3 = boto3.client("s3")

def save_first_page(pdf_path, report_id):
    pages = convert_from_path(pdf_path, dpi=400, first_page=1, last_page=1)
    if not pages:
        raise RuntimeError("No pages rendered.")
    
    image = pages[0].convert("RGB")
    filename = f"{report_id}_p1.jpg"
    s3_key = f"{S3_PAGE_IMG_PREFIX}{filename}"

    # 메모리 버퍼로 S3 업로드
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)
    
    try:
        s3.upload_fileobj(buffer, S3_BUCKET, s3_key)
        print(f"✅ S3 업로드 완료 → s3://{S3_BUCKET}/{s3_key}")
    except Exception as e:
        print(f"❌ S3 업로드 실패: {e}")

    return image  


