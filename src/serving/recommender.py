# src/serving/recommender.py
# 教學說明：推薦核心類別
from __future__ import annotations
from typing import List, Dict
import joblib
import os

class Recommender:
    def __init__(self, model_type: str = "popularity"):
        model_path = "models/popularity.pkl"
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"模型不存在：{model_path}")
        self.items = joblib.load(model_path)

    def recommend(self, user_id: int, top_k: int = 10) -> List[Dict]:
        top_k = min(top_k, 50)
        return [{"item_id": int(i), "score": 1.0} for i in self.items[:top_k]]
