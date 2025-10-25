# tests/unit/test_recommender.py
import os
import joblib
from src.serving.recommender import Recommender

def test_recommender():
    os.makedirs("models", exist_ok=True)
    joblib.dump([1, 2, 3], "models/popularity.pkl")
    rec = Recommender()
    result = rec.recommend(999, 2)
    assert len(result) == 2
    assert result[0]["item_id"] == 1
