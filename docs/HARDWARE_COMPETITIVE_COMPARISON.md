# Hardware competitive comparison — GPU · CPU · RAM

**Date:** 2026-08-04  
**Principle:** Same honesty bar as beat-CUDA: name the opponent, name the metric, state win/loss, do not claim end-to-end where only operator microbenches exist.

---

## 1. What “beat CUDA” already established (GPU)

**Opponent (industry):** dense softmax CUDA attention + PyTorch fused causal SDPA  
**FSOT path:** compact-active consensus (collapse θ, coherence gate, no exp)  
**Device:** RTX 5070 · ledger `Desktop/gpu…/results/competitive/beat_cuda.json`

| Metric | Industry | FSOT | Result |
|--------|----------|------|--------|
| Work complexity | \(O(H S^2 D)\) dense | \(O(H S A D)\), \(A \ll S\) | Structure win |
| Wall-clock vs dense softmax CUDA | baseline | up to **~89×** faster | **WIN** 9/9 shapes |
| Wall-clock vs fused SDPA | baseline | **~1.1–8×** faster | **WIN** 9/9 shapes |
| Active key fraction | ~100% dense | mean \(A_\mathrm{frac} \approx 1.8\%\) | under \(\phi^{-4}\) |

**Claim class:** beat the **industry CUDA algorithm stack** on the attention operator — not “abandon NVIDIA silicon.”

---

## 2. What is the equivalent competitor for CPU?

| Layer | Industry competitor (fair) | FSOT counterpart | Status |
|-------|----------------------------|------------------|--------|
| **Attention algorithm** | Dense softmax attention on **CPU** (NumPy / PyTorch CPU / oneDNN matmul) | Collapse + coherence gate + consensus (no exp), \(O(S\cdot A)\) work | **Complexity win measured**; **wall-clock not yet won** without optimized kernels |
| **Measurement law** | Free temperature / softmax scale knobs | \(\theta = C_\mathrm{eff}\cdot P_\mathrm{var}\), gate \(=\tfrac12\) | **Seed residual 0%** (bare metal + Lean) |
| **Warp / work unit** | 32-wide SIMD / AVX lanes (industry convention) | `states_per_u64 = 32` trit pack | **Exact structural match** |
| **Host scalar engine** | ad-hoc f64 loops | no_std Rust / QEMU boot scalar | **Parity PASS** vs archive |

### CPU — work reduction (theory + GPU ledger, portable)

Same law as CUDA:

\[
W_\mathrm{dense} = H\cdot S^2\cdot D,\qquad
W_\mathrm{FSOT} = H\cdot S\cdot A\cdot D,\qquad
\frac{W_\mathrm{dense}}{W_\mathrm{FSOT}} \approx \frac{S}{A} = \frac{1}{A_\mathrm{frac}}
\]

From beat-CUDA shapes (same \(A_\mathrm{frac}\) law applies on CPU if implemented):

| S | typical \(A_\mathrm{frac}\) | theory upper vs dense |
|---|----------------------------|------------------------|
| 32 | ~8% | ~12× |
| 128 | ~0.8% | ~125× |
| 1024 | ~0.7% | ~140× |

**Mean work efficiency** \(\eta = \mathrm{speedup}\cdot A_\mathrm{frac}\) on GPU suite ≈ **0.33 ≤ 1** (kernel overhead honest, not free-param folded).

### CPU — wall-clock microbench honesty (this machine)

A **pure Python/NumPy** FSOT consensus prototype vs **NumPy dense softmax** on host (2026-08-04):

| H | S | D | FSOT (ms) | Dense CPU (ms) | speedup |
|---|---|---|-----------|----------------|---------|
| 8 | 32 | 16 | 3.1 | 0.24 | **0.08×** (lose) |
| 8 | 128 | 64 | 11.9 | 3.2 | **0.27×** (lose) |
| 4 | 512 | 64 | 24.1 | 21.7 | **0.9×** (lose / near) |

**Why this does not contradict GPU wins:**  
CUDA beat used **native compact kernels** + reduced \(A\). Host NumPy dense matmul is highly optimized BLAS; the Python FSOT path is still a **loopy prototype**. Closing the CPU wall-clock gap means a **Rust/C SIMD compact-active kernel** (same class as `fsot_beat_cuda.cu`), not a residual fold.

**CPU competitive status:**

| Axis | Verdict |
|------|---------|
| Seed law / gates / pack / bare metal | **PASS** (verified) |
| Asymptotic work vs dense softmax | **WIN** (theory + \(A_\mathrm{frac}\) measured) |
| Host wall-clock vs BLAS dense softmax | **OPEN** (needs optimized kernel) |

**Named industry bars for the next climb:**

1. **NumPy / PyTorch CPU** dense causal softmax (same shapes as beat-CUDA)  
2. **oneDNN / MKL** attention-like GEMM baseline  
3. Optional: **llama.cpp** / **OpenVINO** softmax attention micro-op (same H,S,D)

---

## 3. What is the equivalent competitor for RAM?

RAM is **not** “beat DRAM GHz.” The fair industry stack is **layout + density + capacity accounting**:

| Axis | Industry competitor | FSOT | Measured / residual |
|------|---------------------|------|---------------------|
| **State packing** | 1 trit ≈ 1 **byte** (i8/u8) or 4 **bytes** (f32) | **2 bits / trit** → 32 / u64 | **×4 vs u8**, **×16 vs f32** (exact) |
| **Layout** | Opaque heap / CUDA allocator blob | Crystal sectors: header \| boot \| trinary \| Φ \| LTM \| interop | **6 sectors** formal + present |
| **Capacity law** | Datasheet “12 GB” marketing | `usable = C_eff · formal_boundary` (12800 MiB formal) | **0.262%** vs probe 12226.56 MiB |
| **Safety** | runtime OOM | `fits(alloc) ⇔ alloc ≤ formal` | **PASS** on measured VRAM |
| **Identity** | framework-specific tensors | pack∘unpack golden word | **exact** (`5270498306774157604` host = GPU golden) |
| **Host DRAM class** | OS-reported ~32 GiB | \(2^k\) class ±12.5% OS reserve | **PASS** (~31.6 GiB class 32) |

### RAM density example (1e6 trinary states)

| Storage model | Bytes |
|---------------|------:|
| FSOT 2-bit trit bank | **250 000** |
| Industry u8 / i8 per state | 1 000 000 |
| Industry f32 “fluid” state | 4 000 000 |

**Density win vs u8: 4× · vs f32: 16×** — structural, seed-closed, already residual-gated and bare-metal checked.

**What RAM is *not* claiming yet:**

- Higher DDR5 MT/s than JEDEC product  
- Lower latency than L1/L2 industry caches without a cache hierarchy panel  
- Beating cuMemAlloc throughput as a pure memcpy microbench  

Those are **bandwidth** competitors; FSOT’s win class here is **information density + verified layout + seed capacity**, parallel to “skip dead keys” on GPU.

---

## 4. Side-by-side scoreboard

| Domain | Industry bar | FSOT result | Competitive status |
|--------|--------------|-------------|--------------------|
| **GPU attention** | Dense softmax CUDA + fused SDPA | up to 89× / 1.1–8×, 9/9 | **BEAT** (locked suite) |
| **CPU attention work** | Dense \(O(S^2)\) | \(O(S\cdot A)\), \(A\sim1\%\) | **BEAT (complexity)** |
| **CPU attention wall-clock** | NumPy/BLAS dense | Python prototype slower | **OPEN** → Rust SIMD kernel |
| **RAM packing** | u8 / f32 state banks | 2-bit trit, ×4 / ×16 | **BEAT (density)** |
| **VRAM capacity model** | opaque “12 GB” | \(C_\mathrm{eff}\times\) formal boundary | **MATCH ≤0.5%** residual |
| **Bare-metal execute** | often host-only demos | QEMU + host Rust markers | **PASS** multiprover |

---

## 5. How this maps to “what we went out to beat”

| Campaign | Named opponent | Outcome |
|----------|----------------|---------|
| FSOT-GPU | Industry **CUDA attention algorithms** | Beat dense + SDPA on preregistered shapes |
| Processor function | Industry **dense CPU attention / free measurement knobs** | Law + complexity win; wall-clock climb open |
| RAM function | Industry **byte/float state bags + opaque allocators** | Density + crystal capacity win |

GPU answered: *“Can FSOT decide what not to compute on the same silicon?”* → **yes.**  
CPU still needs: *“Can an optimized host kernel realize that smaller work?”* → **not yet measured as wall-clock win.**  
RAM answered: *“Can memory be denser and lawfully sized without free layout parameters?”* → **yes (structural).**

---

## 6. Next competitive climbs (ordered)

1. **CPU beat suite** (mirror `beat_cuda_suite.py`): Rust SIMD compact-active vs NumPy/PyTorch CPU dense softmax, same 9 shapes — lock ledger under `data/competitive_cpu_beat.json`.  
2. **Host DRAM bandwidth** process gate only if seed-linked (optional; do not free-fit GiB/s).  
3. **Cache hierarchy** L1/L2/shared as crystal sector latencies (next RAM depth).  
4. Keep GPU mid-S vs FlashAttention class open (already documented in FSOT-GPU).

---

## 7. Reproduce

```powershell
# GPU (Desktop FSOT-GPU lab)
# .\scripts\build_beat_cuda.ps1; python competitive\beat_cuda_suite.py

# Verified hardware residual + bare metal
python scripts/run_fsot_hardware_bare_metal.py
python scripts/build_fsot_gpu_cuda_bridge.py

# Lean residual panels
# data/fsot_processor_function_panel_benchmark.json
# data/fsot_ram_function_panel_benchmark.json
# data/fsot_gpu_cuda_competitive_panel_benchmark.json
```

**Reports:**  
`data/fsot_hardware_bare_metal_report.json` · `data/cross_proof_verification_report.json` · FSOT-GPU `results/competitive/BEAT_CUDA_REPORT.md`
