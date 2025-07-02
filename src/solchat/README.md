# 21-iceT-ai
21-iceT-ai


### 로컬 실행 방법
```
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
python -m src.main
```

### 파일 구조
```
21-ICET-AI/
├── docs/
│   ├── algorithm/
│   │   ├── backtracking/
│   │   ├── binary_indexed_tree/
│   │   ├── bitwise/
│   │   ├── ...
│   │   └── two_pointer/
│   └── library/
│       ├── cpp/
│       ├── java/
│       └── python/
│           ├── python_library_bisect.md
│           ├── python_library_calculation.md
│           ├── ...
│           └── python_library_summary.md
├── script/
│   ├── create_vectorstore.py
│   └── upload_to_gcs.py
├── src/
│   ├── adapters/
│   │   └── v2/
│   │       ├── llm_client_v2.py
│   │       ├── llm_feedback.py
│   │       ├── llm_interview.py
│   │       └── llm_summary.py
│   ├── core/
│   │   ├── utils/
│   │   │   ├── history_utils.py
│   │   │   └── stream_utils.py
│   │   ├── v1/
│   │   │   └── prompt_templates.py
│   │   └── v2/
│   │       ├── chat_prompt_templates.py
│   │       ├── prompt_templates_v2.py
│   │       ├── embedding_model.py
│   │       ├── exception_handlers.py
│   │       ├── llm_key_manager.py
│   │       ├── logger.py
│   │       └── vector_store.py
│   ├── crawler/
│   │   ├── v1/
│   │   │   ├── boj_crawler.py
│   │   │   ├── pipeline.py
│   │   │   ├── post_client.py
│   │   │   ├── request_mapper.py
│   │   │   └── solution_generater.py
│   │   └── v2/
│   │       ├── boj_crawler_v2.py
│   │       ├── pipeline_v2.py
│   │       ├── post_client_v2.py
│   │       ├── request_mapper_v2.py
│   │       ├── solution_generater_v2.py
│   │       └── daily_crawler.py
│   ├── data/
│   │   ├── boj.csv
│   │   ├── boj.sql
│   │   ├── clean.sql
│   │   ├── export_category_csv.py
│   │   ├── export_problem_csv.py
│   │   └── merge_problem_tags.py
│   ├── recommend/
│   │   ├── problem_loader.py
│   │   ├── recommend_service.py
│   │   └── recommend_service_v2.py
│   ├── routers/
│   │   ├── v1/
│   │   │   └── solution_router.py
│   │   └── v2/
│   │       ├── feedback_router.py
│   │       ├── interview_router.py
│   │       ├── solution_router_v2.py
│   │       └── summary_router.py
│   ├── schemas/
│   │   ├── v1/
│   │   │   └── solution_schema.py
│   │   └── v2/
│   │       ├── feedback_schema.py
│   │       ├── interview_schema.py
│   │       ├── solution_schema_v2.py
│   │       └── summary_schema.py
│   ├── services/
│   │   ├── v1/
│   │   │   └── solution_service.py
│   │   └── v2/
│   │       ├── feedback_service.py
│   │       ├── interview_service.py
│   │       ├── solution_service_v2.py
│   │       └── summary_service.py
│   ├── config.py
│   ├── main.py
│   ├── recommend_daily_pipeline.py
│   └── run_daily_pipeline.py
├── tests/
│   ├── test_solution_generator.py
│   ├── test_solution_generator_v2.py
│   └── test_gradio.py
├── vector/
│   └── faiss_index/
│       ├── index.faiss
│       └── index.pkl
├── .env
├── .gitignore
├── crontab
├── docker-entrypoint.sh
├── Dockerfile
├── README.md
└── requirements.txt
```