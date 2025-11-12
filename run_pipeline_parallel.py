# parallel version placeholder

import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from pipeline.pipeline_parser import run_pipeline_single
from config.paths import PDF_FOLDER

def run_parallel(max_workers=4):
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith(".pdf")]
    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(run_pipeline_single, os.path.join(PDF_FOLDER, f)): f for f in pdf_files}
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"⚠️ Error processing {futures[future]}: {e}")
    return results
