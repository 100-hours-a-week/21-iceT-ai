# 21-iceT-ai
21-iceT-ai

### 변경점
- env, config.py, llm_solution.py도 파라미터 뒤에 _solution 추가
- vector_store.py에서 load_vectorstore() 윈도우 환경 분기
- solution_schema에서 camel style로 통일 후, snake style는 alias 설정
- prompt_templates 에 프롬프트 추가

```
21-ICET-AI/
├── DB/
│   ├── chat_record.csv
│   ├── chat_session.csv
│   └── chat_summary.csv
│
├── docs/
│   ├── algorithm/
│   │   ├── backtracking/
│   │   ├── binary_indexed_tree/
│   │   ├── bitwise/
│   │   ├── ...
│   │   └── two_pointer/
│   │
│   └── library/
│       ├── python_library_bisect.md/
│       ├── python_library_calculation.md/
│       ├── python_library_collections.md/
│       ├── ...
│       └── python_library_summary.md/
│
├── script/
│   ├── create_vectorstore.py
│   └── uproad_to_gcs.py
│
├── src/
│   ├── adapters/
│   │   ├── llm_solution.py
│   │   └── llm_summary.py
│   │
│   ├── core/
│   │   ├── embedding_model.py
│   │   ├── exception_handler.py
│   │   ├── logger.py
│   │   ├── prompt_templates.py
│   │   └── vector_store.py
│   │
│   ├── crawler/
│   │   ├── boj_crawler.py
│   │   ├── daily_crawler.py
│   │   ├── pipeline.py
│   │   ├── post_client.py
│   │   ├── request_mapper.py
│   │   └── solution_generator.py
│   │
│   ├── routers/
│   │   ├── v1
│   │   │   └── solution_router.py
│   │   └── v2/
│   │   │   └── summary_router.py
│   │
│   ├── schemas/
│   │   ├── feedback_schema.py
│   │   ├── interview_schema.py
│   │   ├── solution_schema.py
│   │   └── summary_schema.py
│   │
│   ├── services/
│   │   ├── solution_service.py
│   │   └── summary_service.py
│   │
│   ├── config.py
│   └── main.py
│
├── vector/faiss_index/
│   ├── index.faiss
│   └── index.pkl
│
├── .env
├── app.py
├── daily_runner.py
├── readme.md
└── requirements.txt
```