"""
model_def.py
Definisi arsitektur IndoBERTCNN Dual-Path.
IDENTIK dengan kode di notebook 03_indobert_cnn_training.ipynb.
Jangan ubah class ini tanpa menyesuaikan checkpoint .pt
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModel


class IndoBERTCNN(nn.Module):
    """
    Proposed Model: Dual-Path IndoBERT + CNN 1D.

    Arsitektur:
        BERT → last_hidden_state
                  |
      ┌───────────┴───────────┐
      Path 1: [CLS]     Path 2: CNN multi-kernel
      konteks global    pola n-gram lokal
      Dropout(cls_drop) GlobalMaxPool
      └───── Concatenate ─────┘
             Dropout → Dense(dense_size) → Dropout → Dense(num_classes)

    CNN melengkapi [CLS] — tidak menggantikan.
    Ref: Chen et al. (2020); Devlin et al. (2019); Kim (2014).
    """

    def __init__(
        self,
        bert_model_name: str,
        num_classes: int,
        ngram_sizes: list,
        filter_size: int,
        dropout: float,
        activation: str,
        cls_dropout: float = 0.1,
        dense_size: int = 256,
    ):
        super().__init__()
        self.bert   = AutoModel.from_pretrained(bert_model_name)
        hidden      = self.bert.config.hidden_size  # 768

        def get_act(name):
            if name == "gelu":  return nn.GELU()
            if name == "elu":   return nn.ELU(alpha=1.0)
            return nn.ReLU()

        # Path 2: CNN multi-kernel
        self.convs = nn.ModuleList([
            nn.Sequential(
                nn.Conv1d(hidden, filter_size, kernel_size=k, padding=k // 2),
                get_act(activation),
            )
            for k in ngram_sizes
        ])

        # Path 1: [CLS] dropout
        self.cls_drop = nn.Dropout(cls_dropout)

        # Classifier head setelah concatenate
        combined_dim  = hidden + filter_size * len(ngram_sizes)
        self.drop1    = nn.Dropout(dropout)
        self.fc1      = nn.Linear(combined_dim, dense_size)
        self.act_fc   = get_act(activation)
        self.drop2    = nn.Dropout(dropout)
        self.fc2      = nn.Linear(dense_size, num_classes)

    def forward(self, input_ids, attention_mask):
        bert_out = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        seq      = bert_out.last_hidden_state        # [batch, 128, 768]

        # ── Path 1: [CLS] — konteks global ──────────────────────────────────
        cls_repr = self.cls_drop(seq[:, 0, :])       # [batch, 768]

        # ── Path 2: CNN — pola n-gram lokal ─────────────────────────────────
        x        = seq.permute(0, 2, 1)              # [batch, 768, 128]
        pooled   = [
            F.adaptive_max_pool1d(conv(x), 1).squeeze(-1)
            for conv in self.convs
        ]
        cnn_repr = torch.cat(pooled, dim=1)          # [batch, filter×n_kernels]

        # ── Concatenate + Classifier ─────────────────────────────────────────
        combined = torch.cat([cls_repr, cnn_repr], dim=1)
        x        = self.drop1(combined)
        x        = self.act_fc(self.fc1(x))
        return self.fc2(self.drop2(x))
