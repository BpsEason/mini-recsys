# tests/unit/test_recommender.py
import os
import joblib
from src.serving.recommender import Recommender

def test_recommender():
    # 建立測試用模型
    os.makedirs("models", exist_ok=True)
    joblib.dump([1, 2, 3], "models/popularity.pkl")
    
    rec = Recommender()
    result = rec.recommend(user_id=999, top_k=2)
    
    assert len(result) == 2
    assert result[0]["item_id"] == 1
    assert result[0]["score"] == 1.0
