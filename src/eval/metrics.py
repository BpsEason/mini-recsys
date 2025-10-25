# src/eval/metrics.py
# 教學說明：離線評估指標
# 目前實作：Precision@K, Recall@K
from collections import defaultdict
import numpy as np

def precision_recall_at_k(predictions, k=10, threshold=3.5):
    """
    計算 Precision@K 和 Recall@K
    predictions: List[(uid, iid, true_r, est, _)]
    """
    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))

    precisions = {}
    recalls = {}
    for uid, user_ratings in user_est_true.items():
        # 按預測分數排序
        user_ratings.sort(key=lambda x: x[0], reverse=True)
        # 正向項目（rating >= threshold）
        n_rel = sum((true_r >= threshold) for _, true_r in user_ratings)
        # 前 K 項中預測為正向的
        n_rec_k = sum((est >= threshold) for est, _ in user_ratings[:k])
        # 前 K 項中真正為正向的
        n_rel_and_rec_k = sum(
            (true_r >= threshold) and (est >= threshold)
            for est, true_r in user_ratings[:k]
        )
        # 避免除以 0
        precisions[uid] = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 0
        recalls[uid] = n_rel_and_rec_k / n_rel if n_rel != 0 else 0

    return precisions, recalls
