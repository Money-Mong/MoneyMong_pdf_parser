
# Moneymong PDF Parser

**FastAPI 기반의 PDF 파싱 파이프라인 </br>
MoneyMong 금융 투자 AI 튜터를 위한 RAG 데이터 구축 수행**

## ✅ 주요 기능

* **PDF 파싱 및 구조화**

  * s3에 수집된 애널리스트 리포트 pdf에 대해 layout/image/chunk로 분할 처리
  * text 추출 후 벡터화
* **문서 요약**

  * Document 단위 요약 → 문서 요약 생성
  * Chunk 단위 요약 → 청크 요약 생성
* **NER 개체명 인식**

  * NER을 통해 문서별 주요 기업('main_company'), 산업군('industry'), 종목코드('ticker') 등의 문서 Metadata 저장
* **NER Backfill**

  * 기존 문서에 대해 NER 작업 백필 수행
* **비동기 Task 처리**

  * Task ID로 상태 추적 가능 (`processing`, `completed`, `failed`)
  * 완료 시 Lambda에서 RunPod 종료 요청

---
## ☁️ 파이프라인 구조
```
                          ┌────────────────────────────────┐
                          │   Scheduler (매일 19:00)        │
                          │   or /pdf-parser API Trigger   │
                          └────────────────────────────────┘
                                        │
                                        ▼
                      ┌───────────────────────────────────────┐
                      │    run_db_store_pipeline()            │
                      │    (MoneyMong_pdf_parser)             │
                      └───────────────────────────────────────┘
                                        │
                         [Pending Documents from DB 조회]
                                        │
                                        ▼
                ┌───────────────────────────────────────────────────┐
                │          Download PDF from S3                     │
                │  download_s3_pdf_to_temp(bucket, s3_key)          │
                └───────────────────────────────────────────────────┘
                                        │
                                        ▼
                     ┌────────────────────────────────────┐
                     │       parse_single_pdf()           │
                     └────────────────────────────────────┘
                      │            │             │
      ┌───────────────┘            │             └───────────────────────────┐
      ▼                            ▼                                         ▼
(1) First Page Image      (2) Layout Detection                   (3) Table Detection
save_first_page               detect_layout                          detect_table_crop
      │                            │                                         │
      └───────────────┬────────────┴───────────────────────────────┬─────────┘
                      ▼                                            ▼
                (4) 텍스트 추출                            (5) Text Cleaning
          extract_text(pdf_path, layout_boxes)              clean_text(text)
                      │                                            │
                      ▼                                            ▼
                ┌─────────────────────────────────────────────────────────┐
                │               full_text (문서 전체 텍스트)                  │
                └─────────────────────────────────────────────────────────┘
                                        │
                                        ▼
                         ┌──────────────────────────────────────┐
                         │      (6) 문서 요약 생성 - LLM 호출        │
                         │        summary/doc_summary.py         │
                         │   doc_summary(full_text_clean)        │
                         └──────────────────────────────────────┘
                                        │
                                        ▼
                         ┌──────────────────────────────────────┐
                         │   (7) 문서 단위 NER & 대표기업 추출        │
                         │      extract_main_company()          │
                         └──────────────────────────────────────┘
                                        │
                                        ▼
                         ┌──────────────────────────────────────────┐
                         │     (8) Chunking & Embedding 생성         │
                         │  chunk_and_embed(full_text_clean)        │
                         └──────────────────────────────────────────┘
                                        │
                                        ▼
               ┌────────────────────────────────────────────────────────┐
               │   parse_single_pdf() 최종 결과 result = {                │
               │       "layout_records": [...],                        │
               │       "asset_records": [...],                         │
               │       "chunk_records": [...],                         │
               │       "document_metadata": {...},                     │
               │       "document_summary": {...},                      │
               │   }                                                    │
               └────────────────────────────────────────────────────────┘
                                        │
                                        ▼
		       ┌─────────────────────────────────────────────────────────────────────────────┐
		       │                         insert_pipeline_result()                            │
		       └─────────────────────────────────────────────────────────────────────────────┘
            │              │                │                 │                     │
            ▼              ▼                ▼                 ▼                     ▼
insert_or_update_document  insert_layouts  insert_assets   insert_chunks     insert_summary
                                          
												                      │
												                      ▼
												           Commit (DB 반영 → document, chunks, summary 저장)

```
---

## ⚙️ 시스템 구성도

```
Lambda (crawler) 
     ↓
RunPod API → start A40 Spot Pod   
     ↓ Pod Boot (20~40초)
Lambda → FastAPI /pdf-processing 호출 (POST| https://2mdplr712ixifb-3000.proxy.runpod.net/pdf-processing)
     ↓ 파이프라인 완료
RunPod API → stop Pod
```
---

### 1. pdf-parse

**🙂 오픈 모델 : `"cmarkea/detr-layout-detection”`**
**DETR + PDFminer 결합** 
- DETR로 PDF에 대해 table, image, caption, picture, header, text 등 여러 Label 태그로 레이아웃 파싱
- DETR로 인식한 레이아웃(표,이미지,캡션) 영역을 제외하고, `pdfminer`로 텍스트 추출을 수행
- 테이블은 crop해서 이미지 에셋으로 저장, vlm을 통해 테이블에 대한 정보 저장

<img width="300" alt="Image" src="https://github.com/user-attachments/assets/e9bfd148-6737-4397-af44-72e572155774" />

<img width="300" alt="Image" src="https://github.com/user-attachments/assets/017b7b0d-0602-4f3b-a969-dc750f68d6ae" />




### 2. text chunking, embedding

**🙂 오픈 임베딩 모델 : `sangmini/msmarco-cotmae-MiniLM-L12_en-ko-ja`  ⇒ 추후 OpenAI 4omini 사용 고려**

- 임베딩 벡터 차원과 DB정합성 고려
- 영어, 한국어, 일본에 특화 임베딩 모델

### 3. NER을 통해 문서 개체명 인식

**🙂 오픈 모델 : `“soddokayo/klue-roberta-large-klue-ner”`**

- ELECTRA 기반 모델로 max_position_embeddings=512
- 문서 레벨, 청크 레벨에서 NER을 통해 키워드 및 entities를 제공
- 검색 성능을 높이기 위함
- 청킹에도 NER을 수행해서 RAG 수행시 문서간 cross-inference가 가능하도록
- 메타데이터 컬럼에 저장

```cpp
<엔티티 label>
- OG (기관명)
- DT (날짜)
- QT (수량/단위)
- PS (사람)
- LC(장소)
```

#### OG 한국상장기업명 및 ticker(종목번호) 매핑

1. **KRX_company.csv**
    
    
    | company_name_kr | ticker | industry | aliases |
    | --- | --- | --- | --- |
    
    데이터 : KRX 정보데이터시스템 > 주식 전종목 기본 정보 + 업종분류 현황
    
    [KOSPI, KOSDAQ] 총 2763개 기업 사전 데이터 구성

   
    <img width="700" alt="Image" src="https://github.com/user-attachments/assets/9706eb3f-5f4b-4407-b244-e6250cf7d9a5" />
    </br>     주식 상장 기업 정보를 담은 csv 데이터로 기업 매핑 수행
#### metadata JSONB 예시

- 문서 단위 metadata 예시 - NER
    
    ```json
    {
      "main_company": "미스토홀딩스",
      "main_ticker": "081660",
      "company_scores": [
        {
          "name": "미스토홀딩스",
          "freq": 5,
          "avg_score": 0.96,
          "score": 6.92
        },
        {
          "name": "한화시스템",
          "freq": 1,
          "avg_score": 0.88,
          "score": 2.76
        }
      ]
    }
    
    ```
    
- 청크 단위 metadata 예시 -NER
    
    ```json
    {
      "chunk_orgs": [
        {"name": "아쿠쉬네트", "ticker": null, "score": 0.92}
      ],
      "main_company": "미스토홀딩스"
    }
    
    ```
    

### 4. 문서 요약

**💠 LangChain API 모델 : `ChatUpstage` ⇒ 추후 로컬 모델 Qwen3vl  | openai-o4mini 사용**

- 문서 전체에 대해 간단히 요약 수행 후 document_summary 테이블에 insert 수행

```cpp
<summary>
    <main_topic>피에이치에이의 3분기 실적 및 북미 신공장 가동에 따른 재무 현황과 전망</main_topic>
    <key_points>
        <key_point>북미 매출액은 최근 4개 분기 평균 24% 증가했으나, 영업이익률은 3.3%로 전년 대비 0.8%p 하락했으며, 이는 신공장 가동 초기 비용(인건비 +13%, 감가상각비 +8%) 및 관세 비용 증가로 인한 매출원가율 상승(1.4%p YoY) 때문입니다.</key_point>
        <key_point>미국 신공장(PHA Georgia) 가동으로 PHA America의 분기 평균 매출액은 2024년 4분기~2025년 3분기 730억원(+24% YoY)으로 성장할 전망이며, 현대차 미국 공장에 도어 모듈 및 래치 공급을 확대 중입니다.</key_point>
        <key_point>3분기 누적 기준 매출액 +4% (YoY), 영업이익 -5% (YoY)를 기록했으나, 외환손익 개선으로 세전이익/지배순이익은 각각 9%/26% (YoY) 증가한 145억원/88억원을 달성했습니다.</key_point>
    </key_points>
    <key_terms>
        <key_term>고정비 레버리지 효과: 매출액 증가로 고정비용 분담이 감소하며 수익성 개선되는 현상</key_term>
        <key_term>매출원가율: 매출액 대비 매출원가의 비율로, 원가 효율성 지표</key_term>
        <key_term>영업이익률: 매출액 대비 영업이익 비율로, 영업 효율성 지표</key_term>
    </key_terms>
```

---

## 💠 API 명세

### 📥 POST `/pdf-processing`

RAG 데이터 구축을 위한 비동기 파이프라인 실행

```json
Response:
{
  "task_id": "RUNPOD_TASK_ID",
  "status": "processing_started"
}
```

### 📩 GET `/pdf-status/{task_id}`

특정 task_id에 대한 상태 조회

```json
Response:
{
  "task_id": "RUNPOD_TASK_ID",
  "status": "completed",
  "error": null,
  "updated_at": "2025-11-28T12:34:56"
}
```

### 📤 POST `/summary-backfill`

기존 문서들에 대해 요약 정보 생성 및 저장

### 📤 POST `/ner-backfill`

기존 문서들에 대해 NER 엔터티 메타데이터 백필

---
## 🚀 배포 관리
Docker image 기반 RunPod Pods 컨테이너 구성
#### Pods 사양
<img width="300" height="142" alt="Image" src="https://github.com/user-attachments/assets/c12cf323-7853-49b5-b220-288eb1bfb213" />
</br>

* spot 형태로 과금
* Lambda로 task 완료시 자동으로 Pods Stop 하도록 grpahQL을 통해 비용 절감 수행
* `github Actions` Workflow 로 Docker image 빌드 자동화


---

## 👾 기술 스택

* Python 3.10
* FastAPI
* SQLAlchemy 
* PostgreSQL + PgVector
* AWS Lambda 
* RunPod 
* Huggigface
* Upstage
* PDFMiner
* LangChain


