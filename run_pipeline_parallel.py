import boto3
from concurrent.futures import ProcessPoolExecutor, as_completed
from pipeline.pipeline_parser import run_pipeline_single
from utils.file_loader import download_s3_to_temp
from config.paths import S3_BUCKET, S3_RAW_PREFIX


s3 = boto3.client("s3")

def run_parallel(max_workers=4):
    # S3에서 PDF 파일 목록 검색
    response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=S3_RAW_PREFIX)
    contents = response.get("Contents", [])

    # pdf key만 추출
    pdf_keys = [
        obj["Key"] for obj in contents
        if obj["Key"].lower().endswith(".pdf")
    ]

    # 로컬 임시파일로 다운로드
    local_files = []
    for key in pdf_keys:
        local_path = download_s3_to_temp(S3_BUCKET, key)
        local_files.append((key, local_path))  # (원래 key, 로컬 경로)

    # 병렬 처리 실행
    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(run_pipeline_single, local_path): key
            for key, local_path in local_files
        }

        for future in as_completed(futures):
            key = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"⚠️ Error processing {key}: {e}")

    return results
