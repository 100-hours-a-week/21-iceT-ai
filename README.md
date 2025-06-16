# 21-iceT-ai
가상환경
```
py -3.12 -m venv venv

.\venv\Scripts\Activate.ps1 
```

ngrok 주소 초기화
```
Remove-Item Env:VLLM_URL
```

FastAPI
```
uvicorn src.main:app --reload

python -m src.main
```

Streamlit
```
streamlit run app.py --server.port 8501
```