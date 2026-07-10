//! FSOT Tier 84 executable obligation replay metadata.

use std::path::Path;

/// Total generated obligations (formal + transcendental) from `obligation_meta.json`.
pub fn obligation_count() -> usize {
    let meta_path = Path::new(env!("CARGO_MANIFEST_DIR")).join("obligation_meta.json");
    let Ok(text) = std::fs::read_to_string(meta_path) else {
        return 0;
    };
    let Some(tail) = text.split("\"total_count\":").nth(1) else {
        return 0;
    };
    tail.split(|c: char| !c.is_ascii_digit())
        .find(|s| !s.is_empty())
        .and_then(|s| s.parse().ok())
        .unwrap_or(0)
}