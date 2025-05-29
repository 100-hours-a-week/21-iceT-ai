# 21-iceT-ai
가상환경
```
.\venv\Scripts\activate
```

ngrok 주소 초기화
```
Remove-Item Env:VLLM_URL
```

FastAPI
```
uvicorn src.main:app --reload
```

Streamlit
```
streamlit run app.py --server.port 8501
```

