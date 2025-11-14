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
    
    image = pages[0]
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

    return image  # ⬅️ 이미지 객체(PIL.Image)를 반환


# # save_page.py
# import os
# import io
# import boto3
# import tempfile
# from pdf2image import convert_from_path
# from config.paths import ( S3_BUCKET, S3_PAGE_IMG_PREFIX)

# s3 = boto3.client("s3")

# def save_first_page(pdf_path, report_id):
    
#     # 1페이지만 이미지로 변환
#     pages = convert_from_path(pdf_path, dpi=400, first_page=1, last_page=1)
    
#     if not pages:
#         raise RuntimeError("No pages rendered.")

#     filename = f"{report_id}_p1.jpg"

#     # 메모리 버퍼로 변환 후 S3에 업로드
#     in_memory_file = io.BytesIO()
#     pages[0].save(in_memory_file, format="JPEG")
#     in_memory_file.seek(0)

#     s3_key = f"{S3_PAGE_IMG_PREFIX}{filename}"
#     try:
#         s3.upload_fileobj(in_memory_file, S3_BUCKET, s3_key)
#         print(f"✅ S3 업로드 완료 → s3://{S3_BUCKET}/{s3_key}")
#     except Exception as e:
#         print(f"❌ S3 업로드 실패: {e}")
    
#     local_path = os.path.join(tempfile.gettempdir(), filename)
#     pages[0].save(local_path)

#     return local_path

