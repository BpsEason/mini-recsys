# Mini-RecSys 教學專案

**Mini-RecSys** 是一個專為教學設計的端到端推薦系統專案，帶領學生從原始資料到上線 API 的完整流程。適用於實作實驗課程：資料讀取與切分、基線模型訓練、離線評估、模型序列化、FastAPI 部署與 Docker 容器化。所有程式碼皆包含**正體中文教學註解**，並搭配最小化測試資料與 CI，確保學生可快速上手。

---

## 學習目標

- 執行可重現的機器學習流程：讀取 → 切分 → 訓練 → 評估 → 部署  
- 實作並比較推薦策略：人氣基線 → k-NN → 矩陣分解  
- 理解 Top-K 推薦評估：Precision@K、Recall@K、NDCG 基礎  
- 練習工程最佳實務：模型中繼資料、序列化、單元測試、Docker、輕量 CI  
- 學習生產環境意識：輸入驗證、請求限制（`top_k`）、產物管理、可重現性

---

## 快速開始

### 1. 環境準備（建議）
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2. 最小化流程（快速體驗）
```bash
python -m src.preprocess.split --method loo
python -m src.train.train_popularity
uvicorn src.serving.app:app --reload
```
→ 開啟瀏覽器：http://localhost:8000/docs

### 3. 一鍵啟動腳本
```bash
chmod +x setup.sh
./setup.sh
```

### 4. 執行測試
```bash
pytest tests/unit -v
```

### 5. Docker 部署
```bash
docker build -t mini-recsys .
docker run -p 8000:8000 mini-recsys
# 或
docker-compose up --build
```

---

## 專案結構與重要檔案

```
data/raw/               # 原始資料與小型測試資料（不提交大檔）
data/processed/         # 產生的 train/test CSV（.gitignore）
src/preprocess/split.py # 資料讀取與切分工具（LoO 與時間切分）
src/train/train_popularity.py # 人氣基線訓練器
                              # → 輸出 models/popularity.pkl + metadata.json
src/eval/metrics.py     # 離線評估工具（Precision@K、Recall@K）
src/serving/recommender.py # 推薦核心邏輯：載入模型 + recommend()
src/serving/app.py      # FastAPI 服務：/healthz 與 /recommend
models/                 # 序列化模型（.gitignore）
tests/unit/             # 單元測試（CI 執行）
Dockerfile              # 容器化建置
docker-compose.yml      # 本地編排
.github/workflows/ci.yml # 輕量 CI：生成 fixture 並執行測試
```

---

## 模組教學指引（實驗檢查清單）

### 1. 資料切分（30–45 分鐘）
- **學習目標**：執行切分腳本，檢查輸出檔案
- **任務**：
  ```bash
  python -m src.preprocess.split --method loo
  ```
  - 檢視 `data/processed/train.csv` 與 `test.csv`
  - 練習：比較 LoO 與時間切分（tiny fixture）
- **驗收標準**：`test.csv` 筆數 = 使用者數 × `test_size`

---

### 2. 基線訓練（30–45 分鐘）
- **學習目標**：訓練並儲存人氣模型與中繼資料
- **任務**：
  ```bash
  python -m src.train.train_popularity
  ```
  - 檢視 `models/popularity.pkl` 與 `metadata.json`
- **驗收標準**：模型存在，中繼資料包含 `model_type` 與 `trained_at`

---

### 3. 離線評估（45–60 分鐘）
- **學習目標**：計算 Precision@K 與 Recall@K，理解排序與門檻
- **任務**：
  - 使用 `src/eval/metrics.py` 撰寫評估腳本（或 notebook）
  - 選做：與 toy k-NN 模型比較
- **驗收標準**：輸出 Precision@10 / Recall@10 報告並解釋基線限制

---

### 4. API 與部署（30 分鐘）
- **學習目標**：啟動 FastAPI，呼叫推薦端點
- **任務**：
  ```bash
  uvicorn src.serving.app:app --reload
  ```
  - 測試 `/healthz` 與 `/recommend?user_id=1&top_k=5`
- **驗收標準**：健康檢查回傳 200，推薦回傳長度為 `top_k` 的 JSON

---

### 5. 測試與 CI（30 分鐘）
- **學習目標**：執行單元測試，理解 CI fixture 機制
- **任務**：
  ```bash
  pytest tests/unit -v
  ```
  - 閱讀 `.github/workflows/ci.yml` 了解 fixture 生成
- **驗收標準**：本地測試通過，CI 流程一致

---

### 6. 進階實驗（選修）
- 實作 item-based k-NN（`surprise.KNNBasic`），新增 `train_knn.py`
- 實作矩陣分解（SVD / ALS），搭配 MLflow 追蹤
- 在 `metrics.py` 加入 NDCG@10
- 為 `/recommend` 加入快取或限流機制

---

## API 規格

- **GET /healthz**
  - 模型載入成功 → `200 OK`
  - 否則 → `503` + 錯誤訊息

- **GET /recommend?user_id=&top_k=**
  - **驗證**：`user_id >= 1`；`1 <= top_k <= 50`
  - **回傳**：`[{ "item_id": int, "score": float }]`，長度 ≤ `top_k`

---

## 評分與驗收標準（教師檢查表）

| 項目 | 標準 |
|------|------|
| M1 快速開始 | 學生 60 分鐘內可執行流程並呼叫 `/recommend` |
| M2 基線可重現 | 兩次訓練產生相同 `popularity.pkl`，中繼資料含 pandas 版本與時間戳 |
| M3 測試與 CI | `tests/unit` 通過，CI 能生成 fixture 並執行相同測試 |
| M4 模型中繼資料 | 每個模型皆有對應 JSON，記載 `model_type`、`top_n`、`trained_at`、套件版本 |

---

## 常見問題排除

| 問題 | 解法 |
|------|------|
| `ModuleNotFoundError` | 使用 `uvicorn src.serving.app:app` 或 `python -m` 執行 |
| `FileNotFoundError: train.csv` | 先執行 `src.preprocess.split` 或確認 `data/raw/u.data` 存在 |
| API 503 模型未載入 | 先執行訓練腳本，確認 `models/popularity.pkl` 存在 |
| CI 安裝失敗 | CI 僅安裝最小依賴；若擴充測試，請分離 unit/integration 流程 |

---

## 作業與練習

- **作業 A**：以 item-based k-NN 取代人氣基線  
  → 交付：`train_knn.py` + Precision@10 比較報告  
- **作業 B**：在 `metrics.py` 實作 NDCG@10  
  → 交付：評估 notebook + 排名指標比較圖  
- **作業 C**：新增 `/batch_recommend` 支援多使用者  
  → 交付：API 測試 + 效能考量文件  
- **加分題**：使用 FAISS 建立項目嵌入索引，比較延遲

---

## 貢獻與教學建議

- `requirements.txt` 為課程環境唯一來源，建議學期內鎖定版本  
- 建議使用兩分支：`starter`（學生）與 `solution`（教師）  
- 鼓勵學生提交 PR，CI 即時回饋  
- 評分建議：功能（50%）、測試（20%）、文件（20%）、程式清晰（10%）

---

## 授權

建議使用 [MIT License](LICENSE)（適用於教學材料），請在 `README.md` 中標註。

---

> **Fork 本專案，開始你的推薦系統教學之旅！**
```

