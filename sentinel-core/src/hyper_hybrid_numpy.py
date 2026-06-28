#!/usr/bin/env python3
"""
Hyper‑Hybrid Model – Pure NumPy version (no PyTorch)
- RNN cells
- Multi‑head Latent Attention (MLA)
- Glitch compression (crypto hash + embeddings)
"""

import numpy as np
import hashlib
from typing import List, Optional, Tuple

# ----------------------------------------------------------------------
# 1. Glitch Compression (crypto + embedding)
# ----------------------------------------------------------------------
class GlitchCompressor:
    def __init__(self, vocab_size: int, embed_dim: int = 128, use_hash: bool = True):
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.use_hash = use_hash
        # Random embedding matrix (vocab_size × embed_dim)
        self.embedding = np.random.randn(vocab_size, embed_dim) * 0.01
        # Projection layers (MLP)
        self.proj_W = np.random.randn(embed_dim, embed_dim) * 0.01
        self.proj_b = np.zeros(embed_dim)
        self.proj_W2 = np.random.randn(embed_dim, embed_dim) * 0.01
        self.proj_b2 = np.zeros(embed_dim)
    
    def hash_vector(self, token_ids: List[int]) -> np.ndarray:
        """Deterministic hash embedding from token sequence."""
        combined = "|".join(str(t) for t in token_ids)
        h = hashlib.sha256(combined.encode()).hexdigest()
        # Convert hex to float array of length embed_dim
        byte_arr = bytes.fromhex(h[:self.embed_dim*2])
        float_arr = np.frombuffer(byte_arr, dtype=np.uint8).astype(np.float32) / 255.0
        if len(float_arr) < self.embed_dim:
            float_arr = np.pad(float_arr, (0, self.embed_dim - len(float_arr)))
        else:
            float_arr = float_arr[:self.embed_dim]
        return float_arr
    
    def forward(self, token_ids: List[int]) -> np.ndarray:
        # Embed each token and sum
        emb = np.sum(self.embedding[token_ids], axis=0)   # shape (embed_dim,)
        # MLP
        h = np.tanh(emb @ self.proj_W + self.proj_b)
        comp = h @ self.proj_W2 + self.proj_b2
        if self.use_hash:
            comp = comp + self.hash_vector(token_ids)
        return comp

# ----------------------------------------------------------------------
# 2. Multi‑head Latent Attention (MLA) – NumPy version
# ----------------------------------------------------------------------
class MultiHeadLatentAttention:
    def __init__(self, d_model: int, n_heads: int, latent_dim: Optional[int] = None):
        self.d_model = d_model
        self.n_heads = n_heads
        self.head_dim = d_model // n_heads
        self.latent_dim = latent_dim or (d_model // 2)
        # Query projection
        self.W_q = np.random.randn(d_model, d_model) * 0.01
        # Key/Value projections to latent space
        self.W_k = np.random.randn(d_model, self.latent_dim) * 0.01
        self.W_v = np.random.randn(d_model, self.latent_dim) * 0.01
        # Output projection
        self.W_out = np.random.randn(self.latent_dim, d_model) * 0.01
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """
        x: (seq_len, d_model)  (single batch)
        returns: (seq_len, d_model)
        """
        seq_len = x.shape[0]
        # Q: (seq_len, n_heads, head_dim)
        q = (x @ self.W_q).reshape(seq_len, self.n_heads, self.head_dim)
        # K, V: (seq_len, latent_dim)
        k = x @ self.W_k
        v = x @ self.W_v
        # Scaled dot‑product attention in latent space
        scores = np.einsum('qhd, kd -> qk', q, k) / (self.head_dim ** 0.5)   # (seq_len, seq_len)
        attn = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
        attn = attn / np.sum(attn, axis=-1, keepdims=True)
        context = attn @ v   # (seq_len, latent_dim)
        out = context @ self.W_out   # (seq_len, d_model)
        return out

# ----------------------------------------------------------------------
# 3. RNN Cell (pure NumPy)
# ----------------------------------------------------------------------
class RNNCell:
    def __init__(self, input_dim: int, hidden_dim: int):
        self.Wxh = np.random.randn(hidden_dim, input_dim) * 0.01
        self.Whh = np.random.randn(hidden_dim, hidden_dim) * 0.01
        self.bh = np.zeros(hidden_dim)
    def forward(self, x: np.ndarray, h_prev: np.ndarray) -> np.ndarray:
        # x: (input_dim,), h_prev: (hidden_dim,)
        h = np.tanh(self.Wxh @ x + self.Whh @ h_prev + self.bh)
        return h

# ----------------------------------------------------------------------
# 4. Hybrid Block (selectable RNN or MLA)
# ----------------------------------------------------------------------
class HybridBlock:
    def __init__(self, d_model: int, n_heads: int, mode: str = 'rnn'):
        self.mode = mode
        if mode == 'rnn':
            self.rnn = RNNCell(d_model, d_model)
        else:
            self.attn = MultiHeadLatentAttention(d_model, n_heads)
        # LayerNorm + FFN (simple)
        self.norm_gamma = np.ones(d_model)
        self.norm_beta = np.zeros(d_model)
        self.ffn_W1 = np.random.randn(d_model, 4*d_model) * 0.01
        self.ffn_b1 = np.zeros(4*d_model)
        self.ffn_W2 = np.random.randn(4*d_model, d_model) * 0.01
        self.ffn_b2 = np.zeros(d_model)
    
    def layer_norm(self, x: np.ndarray) -> np.ndarray:
        mean = np.mean(x)
        var = np.var(x)
        return (x - mean) / np.sqrt(var + 1e-5) * self.norm_gamma + self.norm_beta
    
    def ffn(self, x: np.ndarray) -> np.ndarray:
        h = np.maximum(0, x @ self.ffn_W1 + self.ffn_b1)  # ReLU
        return h @ self.ffn_W2 + self.ffn_b2
    
    def forward(self, x: np.ndarray, state: Optional[np.ndarray] = None) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        if self.mode == 'rnn':
            # x: (d_model,) ; state: (d_model,)
            h = self.rnn.forward(x, state)
            residual = h
        else:
            # x: (seq_len, d_model)
            attn_out = self.attn.forward(x)
            residual = attn_out + x
            # For compatibility with single‑step, we keep x as is
            if x.ndim == 1:
                x = x.reshape(1, -1)
                attn_out = self.attn.forward(x)
                residual = attn_out.squeeze(0) + x.squeeze(0)
            else:
                residual = attn_out + x
        normed = self.layer_norm(residual)
        ffn_out = self.ffn(normed)
        out = ffn_out + normed
        new_state = h if self.mode == 'rnn' else None
        return out, new_state

# ----------------------------------------------------------------------
# 5. Hyper‑Hybrid Model (pure NumPy)
# ----------------------------------------------------------------------
class HyperHybridModel:
    def __init__(self, vocab_size: int, d_model: int = 128, n_heads: int = 4, num_layers: int = 3):
        self.d_model = d_model
        self.embedding = np.random.randn(vocab_size, d_model) * 0.01
        self.blocks = []
        for i in range(num_layers):
            mode = 'rnn' if i % 2 == 0 else 'mla'
            self.blocks.append(HybridBlock(d_model, n_heads, mode=mode))
        self.out_proj = np.random.randn(d_model, vocab_size) * 0.01
        self.compressor = GlitchCompressor(vocab_size, d_model)
        self.rnn_states = [None] * num_layers
        self.vocab_size = vocab_size
    
    def reset(self):
        for i, blk in enumerate(self.blocks):
            if blk.mode == 'rnn':
                self.rnn_states[i] = np.zeros(self.d_model)
            else:
                self.rnn_states[i] = None
    
    def forward_step(self, token_id: int) -> np.ndarray:
        """Token ID → logits (vocab_size,)"""
        x = self.embedding[token_id]   # (d_model,)
        for i, blk in enumerate(self.blocks):
            if blk.mode == 'rnn':
                x, new_state = blk.forward(x, state=self.rnn_states[i])
                self.rnn_states[i] = new_state
            else:
                # MLA expects sequence; for single token, add dummy seq dim
                x_seq = x.reshape(1, -1)
                x_seq, _ = blk.forward(x_seq, state=None)
                x = x_seq.squeeze(0)
        logits = x @ self.out_proj   # (vocab_size,)
        return logits
    
    def compress_and_predict(self, token_sequence: List[int]) -> np.ndarray:
        """Compress a sequence of tokens into one compressed vector, then run through hybrid."""
        comp_vec = self.compressor.forward(token_sequence)   # (d_model,)
        x = comp_vec   # treat as a single token embedding
        # Pass through hybrid layers (single step)
        for i, blk in enumerate(self.blocks):
            if blk.mode == 'rnn':
                x, new_state = blk.forward(x, state=self.rnn_states[i])
                self.rnn_states[i] = new_state
            else:
                x_seq = x.reshape(1, -1)
                x_seq, _ = blk.forward(x_seq, state=None)
                x = x_seq.squeeze(0)
        logits = x @ self.out_proj
        return logits

# ----------------------------------------------------------------------
# 6. Demo / Test
# ----------------------------------------------------------------------
if __name__ == "__main__":
    np.random.seed(42)
    vocab_size = 500
    model = HyperHybridModel(vocab_size, d_model=64, n_heads=2, num_layers=3)
    model.reset()
    print("Model created (NumPy). Testing forward step:")
    for t in range(5):
        tok = np.random.randint(0, vocab_size)
        logits = model.forward_step(tok)
        print(f"Token {tok:3d} → logits shape {logits.shape}")
    # Compression test
    seq = [np.random.randint(0, vocab_size) for _ in range(200)]
    logits2 = model.compress_and_predict(seq)
    print(f"\nCompressed 200 tokens → logits shape {logits2.shape}")
    print("Predicted token:", np.argmax(logits2))
