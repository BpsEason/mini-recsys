# src/preprocess/split.py
# 教學說明：資料切分模組
# 功能：讀取 MovieLens u.data，執行 leave-one-out 切分
# 輸出：data/processed/train.csv, test.csv
import pandas as pd
import os

def load_ratings(data_path="data/raw/u.data"):
    """
    讀取 MovieLens 原始資料
    欄位：user_id, item_id, rating, timestamp
    """
    return pd.read_csv(data_path, sep='\t', names=['user_id', 'item_id', 'rating', 'timestamp'])

def leave_one_out_split(df, test_size=1):
    """
    每個使用者保留最後 test_size 筆作為測試集
    其餘作為訓練集（模擬真實推薦場景）
    """
    df = df.sort_values(['user_id', 'timestamp'])
    test = df.groupby('user_id').tail(test_size).copy()
    train = df.drop(test.index).copy()
    return train, test

if __name__ == "__main__":
    df = load_ratings()
    train, test = leave_one_out_split(df)
    os.makedirs("data/processed", exist_ok=True)
    train.to_csv("data/processed/train.csv", index=False)
    test.to_csv("data/processed/test.csv", index=False)
    print(f"切分完成！Train: {len(train)} 筆, Test: {len(test)} 筆")
