# src/train/train_popularity.py
# 教學說明：人氣推薦模型（Baseline）
# 原理：統計 item 評分次數，取前 100 名
import pandas as pd
import joblib
import os
import json
from datetime import datetime

def train():
    train_path = "data/processed/train.csv"
    if not os.path.exists(train_path):
        raise FileNotFoundError(f"找不到訓練資料：{train_path}")
    train = pd.read_csv(train_path)
    popularity = train['item_id'].value_counts().head(100)
    os.makedirs("models", exist_ok=True)
    model_path = "models/popularity.pkl"
    joblib.dump(popularity.index.tolist(), model_path)
    metadata = {
        "model": "popularity",
        "top_n": 100,
        "train_samples": len(train),
        "unique_items": train['item_id'].nunique(),
        "trained_at": datetime.utcnow().isoformat() + "Z"
    }
    with open("models/metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"模型儲存：{model_path}")

if __name__ == "__main__":
    train()
