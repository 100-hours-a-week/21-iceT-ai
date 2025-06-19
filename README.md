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

**env**
```
Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force
```