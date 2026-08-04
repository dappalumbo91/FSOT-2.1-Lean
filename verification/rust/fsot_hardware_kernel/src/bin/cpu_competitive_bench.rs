//! Rust CPU same-class bench: dense softmax vs FSOT compact consensus.
//! Reduces β_f vs Python for small-S; primary metric still work_ratio.

use fsot_hardware_kernel::cpu_competitive::{
    dense_softmax, fsot_compact, work_dense, work_fsot,
};
use std::time::Instant;

fn bench_shape(h: usize, s: usize, d: usize, seed: u64) {
    let n = h * s * d;
    let mut q = vec![0.0f64; n];
    let mut k = vec![0.0f64; n];
    let mut v = vec![0.0f64; n];
    let mut state = seed;
    for i in 0..n {
        state = state.wrapping_mul(6364136223846793005).wrapping_add(1);
        let r = (state >> 33) as f64 / (u32::MAX as f64) * 2.0 - 1.0;
        q[i] = r;
        state = state.wrapping_mul(6364136223846793005).wrapping_add(1);
        k[i] = (state >> 33) as f64 / (u32::MAX as f64) * 2.0 - 1.0;
        state = state.wrapping_mul(6364136223846793005).wrapping_add(1);
        v[i] = (state >> 33) as f64 / (u32::MAX as f64);
    }
    let mut out_d = vec![0.0; n];
    let mut out_f = vec![0.0; n];

    // warmup
    dense_softmax(&q, &k, &v, h, s, d, &mut out_d);
    let a = fsot_compact(&q, &k, &v, h, s, d, &mut out_f);

    let iters = if s >= 512 { 3 } else { 8 };
    let t0 = Instant::now();
    for _ in 0..iters {
        dense_softmax(&q, &k, &v, h, s, d, &mut out_d);
    }
    let t_d = t0.elapsed().as_secs_f64() / iters as f64 * 1000.0;

    let t0 = Instant::now();
    let mut a2 = a;
    for _ in 0..iters {
        a2 = fsot_compact(&q, &k, &v, h, s, d, &mut out_f);
    }
    let t_f = t0.elapsed().as_secs_f64() / iters as f64 * 1000.0;

    let wd = work_dense(h, s, d);
    let wf = work_fsot(h, s, d, a2);
    let wr = wd / wf.max(1e-12);
    let wall = t_d / t_f.max(1e-12);
    println!(
        "RUST_CPU H={h} S={s} D={d} A_frac={a2:.6} work_ratio={wr:.2} wall_speedup={wall:.3} \
         T_dense_ms={t_d:.4} T_fsot_ms={t_f:.4} work_win={} wall_win={}",
        wf < wd,
        t_f < t_d
    );
}

fn main() {
    println!("FSOT_RUST_CPU_COMPETITIVE same-class dense_softmax vs compact_consensus");
    let shapes = [
        (8, 32, 16),
        (8, 64, 32),
        (8, 128, 64),
        (8, 256, 64),
        (8, 512, 64),
        (4, 1024, 64),
        (2, 2048, 64),
    ];
    for (h, s, d) in shapes {
        bench_shape(h, s, d, 42);
    }
}
