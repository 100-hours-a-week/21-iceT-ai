# 21-iceT-ai
**VM**
```
py -3.12 -m venv venv

.\venv\Scripts\Activate.ps1 
```

**FastAPI**
```
uvicorn src.main:app --reload

python -m src.main
```

**Streamlit**
```
streamlit run app.py --server.port 8501
```

**Colab + ngrok**
```
Remove-Item Env:VLLM_URL
```