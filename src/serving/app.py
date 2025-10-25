# src/serving/app.py
# 教學說明：FastAPI 推薦服務
# 提供 /recommend 與 /healthz
from __future__ import annotations
from typing import List
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from src.serving.recommender import Recommender

app = FastAPI(title="Mini-RecSys API", version="0.1.0")

# 啟動時載入模型
rec = None
try:
    rec = Recommender()
    print("推薦模型載入成功")
except Exception as e:
    print(f"模型載入失敗：{e}")

class RecommendationResponse(BaseModel):
    item_id: int
    score: float

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.get("/recommend", response_model=List[RecommendationResponse])
def recommend(
    user_id: int = Query(..., ge=1, description="使用者 ID"),
    top_k: int = Query(10, ge=1, le=50, description="回傳數量 (1~50)")
):
    if rec is None:
        raise HTTPException(status_code=503, detail="推薦模型尚未載入")
    return rec.recommend(user_id, top_k)
