# 21-iceT-ai
21-iceT-ai

### 변경점
- llm_client.py => llm_solution.py
- env, config.py, llm_solution.py도 파라미터 뒤에 _solution 추가
- vector_store.py에서 load_vectorstore() 윈도우 환경 분기
- prompt_templates 에 프롬프트 추가

<br>

- 

### 명령어 복붙
```
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
python -m src.main
```

### 파일 구조
```
```