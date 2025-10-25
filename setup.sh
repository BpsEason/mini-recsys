#!/bin/bash
echo "開始 Mini-RecSys 教學流程..."
python -m src.preprocess.split
python -m src.train.train_popularity
echo "啟動 API：http://localhost:8000/docs"
uvicorn src.serving.app:app --reload
