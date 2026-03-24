from app.core.logging import setup_logging
from fastapi import FastAPI
setup_logging()
app = FastAPI(title="EduEquity API", version="0.1.0")