# src/train/train_popularity.py
# 教學說明：人氣推薦模型（Baseline）
# 原理：統計每個 item 被評分的次數，取前 100 名
# 輸出：models/popularity.pkl
import pandas as pd
import joblib
import os
import json
from datetime import datetime

def train():
    train_path = "data/processed/train.csv"
    if not os.path.exists(train_path):
        raise FileNotFoundError(f"找不到訓練資料：{train_path}")
    
    print("讀取訓練資料...")
    train = pd.read_csv(train_path)
    
    # 計算人氣：每個 item 的評分次數
    popularity = train['item_id'].value_counts().head(100)
    
    os.makedirs("models", exist_ok=True)
    model_path = "models/popularity.pkl"
    joblib.dump(popularity.index.tolist(), model_path)
    
    # 儲存模型中繼資料
    metadata = {
        "model": "popularity",
        "top_n": 100,
        "train_samples": len(train),
        "unique_items": train['item_id'].nunique(),
        "trained_at": datetime.utcnow().isoformat() + "Z"
    }
    with open("models/metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"人氣模型已儲存：{model_path}（{len(popularity)} 個熱門項目）")

if __name__ == "__main__":
    train()
