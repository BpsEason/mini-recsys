# src/serving/recommender.py
# 教學說明：推薦核心類別
# 目前支援：Popularity 模型
from __future__ import annotations
from typing import List, Dict
import joblib
import os

class Recommender:
    def __init__(self, model_type: str = "popularity"):
        self.model_type = model_type
        model_path = "models/popularity.pkl"
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"模型檔案不存在：{model_path}")
        self.items = joblib.load(model_path)  # List[int]

    def recommend(self, user_id: int, top_k: int = 10) -> List[Dict]:
        """
        為指定使用者推薦 top_k 個項目
        目前：直接回傳全域人氣前 top_k
        """
        top_k = min(top_k, 50)  # 安全上限
        return [
            {"item_id": int(item_id), "score": 1.0}
            for item_id in self.items[:top_k]
        ]
