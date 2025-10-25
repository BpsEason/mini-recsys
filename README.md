### 專案簡介
Mini-RecSys 是教學導向的端到端推薦系統範例，帶領學習者從原始互動資料走完整個 ML 工程流程：資料切分 → 基線訓練（Popularity）→ 離線評估 → 模型序列化 → API 服務化（FastAPI）→ 單元測試與 CI。所有程式檔含正體中文註解、提供小型 fixture，方便課堂示範與學生練習。

學習重點：資料切分策略、Top‑K 評估概念、Baseline 與簡單推薦演算法實作、模型可重現性、服務化與測試/CI 實務。

---

### 快速開始（五分鐘跑通）
1. 建議環境：Python 3.11，建立虛擬環境並安裝依賴  
   ```bash
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```
2. 產生切分資料（若無原始 u.data，會使用 tiny fixture）
   ```bash
   python -m src.preprocess.split --method loo
   ```
3. 訓練人氣基線（Popularity）
   ```bash
   python -m src.train.train_popularity
   ```
4. 啟動 API（開發模式）
   ```bash
   uvicorn src.serving.app:app --reload
   ```
5. 驗證（Swagger UI）
   - 打開： http://localhost:8000/docs  
   - 範例： GET /recommend?user_id=1&top_k=5

一鍵示範（開發用）
```bash
chmod +x setup.sh
./setup.sh
```

---

### 專案結構（要點）
- **data/raw/**：原始或 fixture 資料（請勿把大型原始資料提交至 repo）  
- **data/processed/**：切分後的 train/test（被 .gitignore 忽略）  
- **src/preprocess/split.py**：資料載入與 Leave‑One‑Out / temporal 切分實作  
- **src/train/train_popularity.py**：Popularity baseline 訓練與模型/metadata 儲存  
- **src/eval/metrics.py**：離線評估工具（Precision@K、Recall@K；可擴充 NDCG）  
- **src/serving/recommender.py**：推薦器業務層（載入模型、提供 recommend 接口）  
- **src/serving/app.py**：FastAPI 應用（/healthz、/recommend）  
- **models/**：序列化模型與 metadata（加入 .gitignore，不要上傳敏感檔案）  
- **tests/unit/**：單元測試、CI fixtures  
- **Dockerfile / docker-compose.yml**：容器化設定  
- **.github/workflows/ci.yml**：簡易 CI（建立 fixtures 並跑 unit tests）  
- **README.md、setup.sh**：教學與啟動腳本

---

### 課程模組與實驗步驟（教案化）
每個模組包含學習目標、操作步驟、驗收標準、延伸任務。

1. 模組 1：專案介紹與快速上手（30–45 分）  
   - 目標：在本地 60 分鐘內跑通 pipeline 並呼叫 API。  
   - 步驟：快速開始章節的 1–4 步驟。  
   - 驗收：/healthz 回 200；/recommend 回傳 JSON top‑K。  

2. 模組 2：資料切分與實驗設計（45–60 分）  
   - 目標：理解 LoO 與時序切分差異，能產生 train/test。  
   - 任務：執行 `--method loo` 與 `--method temporal`，比較 test distribution。  
   - 驗收：data/processed/train.csv 與 test.csv 存在，test 大小合理。  

3. 模組 3：Popularity 與基線比較（45–60 分）  
   - 目標：實作並儲存人氣模型，理解 baseline 重要性。  
   - 任務：跑 train_popularity、查看 models/popularity.pkl 與 metadata。  
   - 驗收：模型與 metadata 檔案存在，metadata 包含 trained_at 與 train_samples。  

4. 模組 4：離線評估（60–90 分）  
   - 目標：計算 Precision@K、Recall@K，並解釋指標意義。  
   - 任務：使用 src/eval/metrics.py 撰寫簡單評估腳本，比較 baseline 結果。  
   - 驗收：報告包含 Precision@10/Recall@10 與結論。  

5. 模組 5：擴充演算法（選做，2–4 小時）  
   - 目標：實作 item‑based k‑NN 或 Matrix Factorization，並比較效能。  
   - 任務：加入 src/train/train_knn.py 或 train_mf.py，儲存新模型並更新 recommender。  
   - 驗收：新模型在同一測試集上改善 NDCG 或能說明為何未改善。  

6. 模組 6：部署、測試與 CI（45–90 分）  
   - 目標：理解模型序列化、API 載入與 CI 測試流程。  
   - 任務：閱讀 .github/workflows/ci.yml，執行 pytest tests/unit。  
   - 驗收：unit tests 通過；CI 能在 push 時建立 fixtures 並通過。  

---

### 評分標準（教師用 Rubric）
- 功能性（50%）：能跑通 pipeline，API 返回正確格式（/recommend/top_k）。  
- 測試（20%）：提供至少 3 個單元測試並通過（包含模型載入與推薦行為）。  
- 文件與可重現性（20%）：README 有完整快速啟動與實驗重現步驟；models metadata 完備。  
- 程式碼品質（10%）：註解清楚、結構模組化、無明顯錯誤與硬編碼路徑。

--- 

### Docker、CI 與生產考量（教學要點）
- Docker：使用 Dockerfile 建映像，docker-compose 可在本機模擬多容器。示例：
  ```bash
  docker build -t mini-recsys .
  docker run -p 8000:8000 mini-recsys
  # or
  docker-compose up --build
  ```
- CI：現行 workflow 為 minimal unit 流程（安裝 pandas/pytest/joblib），在 CI 建立 fixtures（小訓練檔與 models/popularity.pkl）後執行 pytest。若需整合 heavy libs（surprise、mlflow），請分成 unit/integration 兩個 workflow 並使用 caching。
- 生產議題（課堂討論）：版本化模型與 metadata、API 速率限制、認證、模型更新策略（Canary/A-B）、向量索引（FAISS）對延展性的影響。

---

### 常見錯誤與排解
- ModuleNotFoundError：確保以 module 跑 uvicorn（uvicorn src.serving.app:app），或將 repo 根目錄加入 PYTHONPATH。  
- FileNotFoundError(train.csv)：先執行 src.preprocess.split，確認 data/raw/u.data 或 tiny fixture 存在。  
- 模型載入失敗：檢查 models/popularity.pkl 是否存在並與當前環境相容（joblib 版本差異會影響反序列化）。  
- CI 失敗：查看 workflow log，確認 fixtures 步驟有建立 data/processed 與 models 檔案。

---

### 延伸閱讀與作業建議
- 實作 item‑based 與 user‑based k‑NN，分析相似度度量對結果影響（cosine vs Pearson）。  
- 實作簡易 NeuMF 或 embedding + MLP，並比較 negative sampling 策略效果。  
- 加入向量索引（FAISS）以提升相似度檢索效能，討論 trade‑off。  
- 設計一個簡單的 A/B 實驗模擬框架（線上指標 vs 離線指標差異）。
